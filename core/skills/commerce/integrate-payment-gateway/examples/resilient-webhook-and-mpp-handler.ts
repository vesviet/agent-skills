/**
 * Resilient Webhook and MPP (HTTP 402) Payment Handler
 *
 * Implements:
 * - Constant-time HMAC SHA-256 raw payload signature verification
 * - 300-second replay attack protection window
 * - Fast queue-first response (<500ms) with distributed deduplication
 * - HTTP 402 / x402 programmatic agent negotiation
 */

import * as crypto from 'crypto';

export interface WebhookEventPayload {
  id: string;
  type: string;
  created: number; // Unix timestamp
  data: {
    object: {
      id: string;
      amount: number;
      currency: string;
      status: string;
      metadata?: Record<string, string>;
    };
  };
}

export interface IngestionQueue {
  enqueue(topic: string, event: WebhookEventPayload): Promise<void>;
}

export interface DistributedLockProvider {
  acquire(key: string, ttlMs: number): Promise<boolean>;
  release(key: string): Promise<void>;
}

export class ResilientPaymentHandler {
  constructor(
    private readonly webhookSecret: string,
    private readonly queue: IngestionQueue,
    private readonly lockProvider: DistributedLockProvider
  ) {}

  /**
   * Verifies raw payload signature using constant-time HMAC comparison.
   */
  public verifyStripeSignature(rawBody: Buffer, signatureHeader: string): boolean {
    const parts = signatureHeader.split(',');
    let timestamp = '';
    let expectedSignature = '';

    for (const part of parts) {
      const [key, value] = part.trim().split('=');
      if (key === 't') timestamp = value;
      if (key === 'v1') expectedSignature = value;
    }

    if (!timestamp || !expectedSignature) {
      return false;
    }

    // Check 300-second replay window
    const eventTime = parseInt(timestamp, 10);
    const currentTime = Math.floor(Date.now() / 1000);
    if (Math.abs(currentTime - eventTime) > 300) {
      return false; // Replay window exceeded
    }

    // Compute expected HMAC digest over raw bytes
    const signedPayload = `${timestamp}.${rawBody.toString('utf-8')}`;
    const computedSignature = crypto
      .createHmac('sha256', this.webhookSecret)
      .update(signedPayload)
      .digest('hex');

    const bufComputed = Buffer.from(computedSignature, 'utf-8');
    const bufExpected = Buffer.from(expectedSignature, 'utf-8');

    if (bufComputed.length !== bufExpected.length) {
      return false;
    }

    return crypto.timingSafeEqual(bufComputed, bufExpected);
  }

  /**
   * Queue-first webhook ingestion endpoint handler.
   */
  public async handleWebhook(
    rawBody: Buffer,
    signatureHeader: string
  ): Promise<{ statusCode: number; message: string }> {
    const startTime = Date.now();

    // 1. Signature Verification
    const isValid = this.verifyStripeSignature(rawBody, signatureHeader);
    if (!isValid) {
      return { statusCode: 400, message: 'Invalid signature or expired replay window' };
    }

    // 2. Parse Event JSON safely after signature check
    const event: WebhookEventPayload = JSON.parse(rawBody.toString('utf-8'));

    // 3. Distributed Deduplication Lock
    const lockKey = `lock:webhook:event:${event.id}`;
    const acquired = await this.lockProvider.acquire(lockKey, 30_000);
    if (!acquired) {
      // Event already being handled concurrently
      return { statusCode: 200, message: 'Event already in processing' };
    }

    try {
      // 4. Offload to Queue for asynchronous background processing
      await this.queue.enqueue('payment.events', event);

      const durationMs = Date.now() - startTime;
      if (durationMs > 500) {
        console.warn(`[PERF ALERT] Webhook ingestion took ${durationMs}ms (>500ms SLA)`);
      }

      return { statusCode: 200, message: 'Enqueued' };
    } finally {
      await this.lockProvider.release(lockKey);
    }
  }

  /**
   * Generates an HTTP 402 Payment Required response for autonomous agent callers (MPP / x402).
   */
  public generateMppChallenge(
    resourceId: string,
    priceUsdc: number,
    depositAddress: string
  ): {
    statusCode: 402;
    headers: Record<string, string>;
    body: Record<string, unknown>;
  } {
    const challengePayload = {
      version: 'x402-v1',
      resource_id: resourceId,
      accepted_currencies: ['USDC-BASE', 'USDC-TEMPO'],
      amount: priceUsdc,
      deposit_address: depositAddress,
      valid_until: Math.floor(Date.now() / 1000) + 900, // 15 min expiry
    };

    const encodedChallenge = Buffer.from(JSON.stringify(challengePayload)).toString('base64');

    return {
      statusCode: 402,
      headers: {
        'Content-Type': 'application/json',
        'Payment-Required': encodedChallenge,
        'WWW-Authenticate': `MPP realm="api", token="${encodedChallenge}"`,
      },
      body: {
        error: 'Payment Required',
        message: 'Resource requires pre-authorized MPP / x402 token or crypto settlement.',
        challenge: challengePayload,
      },
    };
  }
}
