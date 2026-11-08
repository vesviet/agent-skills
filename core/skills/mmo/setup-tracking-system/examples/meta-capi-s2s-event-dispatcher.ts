import * as crypto from 'crypto';

export interface ConversionEvent {
  eventName: 'Purchase' | 'Lead' | 'AddToCart';
  eventId: string; // Shared UUIDv4 for deduplication
  eventTime: number; // Unix epoch seconds
  eventSourceUrl: string;
  userData: {
    email?: string;
    phone?: string;
    fbp?: string;
    fbc?: string;
    clientIp: string;
    clientUserAgent: string;
  };
  customData?: {
    currency: string;
    value: number;
    orderId?: string;
  };
}

export class MetaCapiDispatcher {
  private pixelId: string;
  private accessToken: string;
  private apiVersion = 'v20.0';

  constructor(pixelId: string, accessToken: string) {
    this.pixelId = pixelId;
    this.accessToken = accessToken;
  }

  private hashSha256(value: string): string {
    return crypto.createHash('sha256').update(value.trim().toLowerCase()).digest('hex');
  }

  private normalizePhone(phone: string): string {
    return phone.replace(/[^0-9+]/g, '');
  }

  public async dispatchEvent(event: ConversionEvent): Promise<boolean> {
    const payload = {
      data: [
        {
          event_name: event.eventName,
          event_time: event.eventTime,
          event_id: event.eventId,
          event_source_url: event.eventSourceUrl,
          action_source: 'website',
          user_data: {
            em: event.userData.email ? [this.hashSha256(event.userData.email)] : undefined,
            ph: event.userData.phone ? [this.hashSha256(this.normalizePhone(event.userData.phone))] : undefined,
            fbp: event.userData.fbp,
            fbc: event.userData.fbc,
            client_ip_address: event.userData.clientIp,
            client_user_agent: event.userData.clientUserAgent,
          },
          custom_data: event.customData,
        },
      ],
    };

    const endpoint = `https://graph.facebook.com/${this.apiVersion}/${this.pixelId}/events?access_token=${this.accessToken}`;

    const res = await fetch(endpoint, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const errorText = await res.text();
      console.error(`Meta CAPI error (${res.status}): ${errorText}`);
      return false;
    }

    return true;
  }
}
