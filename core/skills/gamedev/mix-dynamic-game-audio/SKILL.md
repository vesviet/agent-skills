---
name: mix-dynamic-game-audio
description: Architect dynamic game audio hierarchies, bus mixers, sidechain ducking, adaptive music stem crossfading, and pooled 3D positional sound emitters. Use when implementing interactive soundscapes, adaptive music states, or spatial SFX systems.
allowed-tools:
  - read_file
  - write_file
  - edit_file
  - create_file
  - search_code
  - run_build
  - run_tests
  - run_linter
  - execute_command
version: "1.0.0"
---

# Mix Dynamic Game Audio

Design and implement responsive, non-clipping game audio architectures featuring hierarchical bus mixers, sidechain ducking, adaptive music synchronization, and pooled 3D spatial sound emitters.

## Core Rules

- **Hierarchical Bus Routing**: Never play raw audio clips directly to hardware output. Route every sound through an explicit bus tree (`Master` <- `Music`, `SFX`, `Ambience`, `Voice/Dialogue`, `UI`) with independent decibel (`dB`) volume faders and mute states.
- **Voice Stealing & Emitter Pooling**: Pre-allocate a fixed pool of `AudioStreamPlayer` / `AudioSource` instances. Enforce per-cue polyphony caps (e.g., max 4 concurrent footstep or gunshot voices) with priority-based voice stealing to prevent phase cancellation and CPU overload.
- **Micro-Pitch & Volume Randomization**: Apply subtle per-trigger randomization ($\pm 0.05\text{--}0.12$ pitch scale, $\pm 1.5\text{dB}$ volume offset) plus round-robin sample selection to eliminate repetitive "machine-gunning" on rapid SFX.
- **Contract Adherence**: Emit `contracts/schemas/implementation-result.json` upon completing game audio system implementations.

## Suggested Process

### 1. Bus Mixer Topology & Headroom Protection
Configure the master bus hierarchy with logarithmic volume conversion ($\text{dB} = 20 \log_{10}(\text{linear})$):
- Place a peak limiter on the `Master` bus at $-1.0\text{dBFS}$ to prevent digital clipping during intense combat explosions.
- Attach a sidechain compressor/ducker from `Voice/Dialogue` and critical `SFX` onto `Music` and `Ambience` (attenuating background buses by $-6\text{dB}$ to $-9\text{dB}$ with fast attack and $300\text{ms}$ release).

### 2. Pooled 2D/3D Sound Event Dispatcher
Build a centralized audio event manager decoupled from gameplay entities:
- Acquire an idle pooled emitter, assign the audio bank cue, apply pitch/gain jitter, and return the emitter to the pool automatically upon playback completion.

### 3. Positional 3D Attenuation & Occlusion
Configure 3D spatial emitters with physically plausible distance attenuation (logarithmic or inverse-distance rolloff, reference distance, and max audible cutoff) plus low-pass filter (LPF) cutoff modulation when line-of-sight raycasts detect wall occlusion.

### 4. Adaptive Music Stem Crossfading
Synchronize vertical music layers (Ambient, Exploration, Tension, Combat) on shared bar/beat timelines, crossfading stem volumes smoothly across gameplay state transitions without restarting playback heads.

## Output Contracts

When completing dynamic game audio implementation, emit:
- `contracts/schemas/implementation-result.json`

## Checklist

- [ ] All audio emitters route through `Master`, `Music`, `SFX`, `Ambience`, `Voice`, or `UI` buses
- [ ] Sound emitter pooling and per-event polyphony limits prevent voice exhaustion and clipping
- [ ] Repetitive SFX apply round-robin sample selection and pitch/volume micro-randomization
- [ ] Sidechain ducking attenuates music and ambience cleanly during dialogue or heavy impacts
- [ ] 3D spatial emitters configure distance attenuation curves and occlusion low-pass filtering
- [ ] Adaptive music stems transition smoothly across game states without timeline drift

## Related Skills

- **tune-game-feel**: multi-tier impact audio feedback and sound ducking curves
- **manage-scene-lifecycle**: asynchronous audio stream crossfading and bus cleanup across scene transitions
