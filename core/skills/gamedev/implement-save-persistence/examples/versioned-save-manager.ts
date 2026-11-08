import * as fs from 'fs';
import * as path from 'path';
import * as crypto from 'crypto';

export interface SaveEnvelope<T> {
  magic: string;
  schemaVersion: number;
  timestampUtc: number;
  playtimeSeconds: number;
  checksumSha256: string;
  payload: T;
}

export type MigrationStep = (oldPayload: any) => any;

export class VersionedSaveManager {
  private readonly currentVersion: number;
  private readonly migrations: Map<number, MigrationStep> = new Map();
  private readonly saveDirectory: string;

  constructor(saveDir: string, currentVersion: number) {
    this.saveDirectory = saveDir;
    this.currentVersion = currentVersion;
    if (!fs.existsSync(saveDir)) {
      fs.mkdirSync(saveDir, { recursive: true });
    }
  }

  public registerMigration(fromVersion: number, step: MigrationStep) {
    this.migrations.set(fromVersion, step);
  }

  private computeChecksum(payload: any): string {
    const serialized = JSON.stringify(payload);
    return crypto.createHash('sha256').update(serialized).digest('hex');
  }

  public saveSlot(slotName: string, payload: any, playtimeSeconds: number) {
    // Sanitize slot name against path traversal
    if (!/^[a-zA-Z0-9_-]{1,32}$/.test(slotName)) {
      throw new Error(`Invalid slot name: ${slotName}`);
    }

    const envelope: SaveEnvelope<any> = {
      magic: 'GMSV',
      schemaVersion: this.currentVersion,
      timestampUtc: Math.floor(Date.now() / 1000),
      playtimeSeconds,
      checksumSha256: this.computeChecksum(payload),
      payload,
    };

    const targetFile = path.join(this.saveDirectory, `${slotName}.sav`);
    const tempFile = path.join(this.saveDirectory, `${slotName}.sav.tmp`);
    const backupFile = path.join(this.saveDirectory, `${slotName}.sav.bak`);

    // 1. Write to temp file
    fs.writeFileSync(tempFile, JSON.stringify(envelope, null, 2), 'utf-8');

    // 2. Backup existing save if present
    if (fs.existsSync(targetFile)) {
      fs.copyFileSync(targetFile, backupFile);
    }

    // 3. Atomic rename
    fs.renameSync(tempFile, targetFile);
  }

  public loadSlot(slotName: string): any {
    const targetFile = path.join(this.saveDirectory, `${slotName}.sav`);
    const backupFile = path.join(this.saveDirectory, `${slotName}.sav.bak`);

    let raw: string;
    try {
      raw = fs.readFileSync(targetFile, 'utf-8');
    } catch {
      if (fs.existsSync(backupFile)) {
        console.warn(`Primary save missing for ${slotName}. Falling back to .bak.`);
        raw = fs.readFileSync(backupFile, 'utf-8');
      } else {
        throw new Error(`Save slot not found: ${slotName}`);
      }
    }

    const envelope: SaveEnvelope<any> = JSON.parse(raw);

    // Verify magic bytes
    if (envelope.magic !== 'GMSV') {
      throw new Error('Invalid save envelope magic bytes');
    }

    // Verify payload integrity checksum
    const computed = this.computeChecksum(envelope.payload);
    if (computed !== envelope.checksumSha256) {
      if (fs.existsSync(backupFile)) {
        console.warn('Checksum failure! Recovering from .bak.');
        return this.loadSlotFromPath(backupFile);
      }
      throw new Error('Corrupted save payload: checksum mismatch');
    }

    // Run sequential migrations if save is older
    let currentPayload = envelope.payload;
    let version = envelope.schemaVersion;

    if (version > this.currentVersion) {
      throw new Error(`Save version ${version} is newer than game engine version ${this.currentVersion}`);
    }

    while (version < this.currentVersion) {
      const step = this.migrations.get(version);
      if (!step) {
        throw new Error(`Missing migration step for schema version ${version} -> ${version + 1}`);
      }
      currentPayload = step(currentPayload);
      version++;
    }

    return currentPayload;
  }

  private loadSlotFromPath(filePath: string): any {
    const raw = fs.readFileSync(filePath, 'utf-8');
    const envelope: SaveEnvelope<any> = JSON.parse(raw);
    return envelope.payload;
  }
}
