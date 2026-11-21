# Squawk Box

A platform dedicated to detecting, aggregating, and classifying my pet cockatiel's vocalizations.

## Setup

https://wiki.seeedstudio.com/ReSpeaker_2_Mics_Pi_HAT_Raspberry/

### Mixer configuration

With the `seeed-linux-dtoverlays` driver, the WM8960 codec boots with the mic disconnected from the ADC, so `arecord` runs successfully but produces near-silent files. Fix it in `alsamixer` (press `F6` to select the `seeed2micvoicec` card, then `F5` to show all controls), then persist the settings:

```bash
sudo alsactl store
```

alsamixer truncates control names; the `Item:` line at the top shows the full name of the selected control. `MM` under a control means muted/off and `OO` means on; press `M` to toggle.

#### Recording (mic → file)

Listed in signal-path order. Every switch must be on for audio to reach the file.

```
Mic ─► LINPUT1 ─► Boost Mixer LINPUT1 Switch ─► Input Boost Mixer LINPUT1 Volume ─► Input Mixer Boost Switch ─► ADC ─► Capture ─► ADC PCM Capture ─► file
```

| Control | What it does | Suggested setting |
|---|---|---|
| **Left/Right Boost Mixer LINPUT1 / RINPUT1** | Connects each mic to its preamp. The HAT's two mics are wired to input 1 of each side. | On |
| **Left/Right Input Boost Mixer LINPUT1 / RINPUT1** (volume) | Mic preamp gain, in 4 steps: 0 / +13 / +20 / +29 dB. The largest analog gain stage, with the most effect on loudness and noise. | +13 or +20 dB |
| **Left/Right Input Mixer Boost** | Sends the preamp output into the ADC. **Off by default, which causes silent recordings.** | On |
| **Capture** (volume + switch) | Fine analog gain just before the ADC, from −17 to +30 dB. Its mute switch must also be on. | Unmuted, ~60–80% |
| **ADC PCM Capture** | Digital gain after conversion. It just multiplies the numbers, so it amplifies noise too. | ~195 (0 dB) |
| **ADC High Pass Filter** | Removes very low frequencies and the DC offset. | On |

Raise the analog stages first (Input Boost, then Capture) until loud sounds get close to clipping without hitting it. Use ADC PCM Capture only as a last resort.

`arecord` records mono by default, which captures only the left mic. Pass `-c 2` to record both.

##### Automatic gain control (ALC)

ALC continuously adjusts the Capture gain to hold the input near a target level. Leave it off and set gain manually to start.

- **ALC Function**: `Off` / `Left` / `Right` / `Stereo`. Turns ALC on, per channel.
- **ALC Target**: the level it aims for.
- **ALC Max Gain / Min Gain**: limits on how far it can adjust.
- **ALC Attack / Decay / Hold Time**: how quickly it reacts to loud sounds and recovers afterwards.
- **ALC Mode**: `ALC` boosts quiet audio and cuts loud audio; `Limiter` only cuts loud peaks.
- **Noise Gate** (switch + threshold): when ALC is on, silences the input whenever it falls below the threshold.

#### Playback (file → headphone jack / speaker connector)

| Control | What it does |
|---|---|
| **Playback** | Digital master volume for anything played. |
| **Left/Right Output Mixer PCM Playback** (switch) | Connects the DAC to the outputs. If off, nothing is heard. |
| **Headphone** | Volume for the 3.5 mm jack. |
| **Speaker** | Volume for the JST speaker connector. |
| **Speaker AC / DC** | Extra speaker amplifier gain. Raise only if the speaker is too quiet at full volume. |
| **PCM Playback -6dB** | Cuts playback by 6 dB to avoid clipping. Leave off. |

#### Controls to ignore

- **LINPUT2/3, RINPUT2/3** and their switches: those inputs aren't connected on this HAT.
- **Output Mixer Boost Bypass / LINPUT3**: route inputs straight to the outputs, skipping the converters. Only useful for live monitoring, and can cause feedback.
- **Mono Output Mixer**: the HAT doesn't use the chip's mono output.
- **3D, 3D Filter**: stereo-widening effect.
- **DAC Deemphasis, DAC Filter Characteristics**: fine audio-quality tweaks; leave at defaults.
- **ADC/DAC Polarity, ADC Data Output Select, DAC Mono Mix**: channel swapping and inversion, only needed for unusual wiring.
- **ZC (zero-cross) switches**: make volume changes wait for the waveform to cross zero, avoiding clicks.

### Recording

Record a 5-second stereo test clip at 48 kHz:

```bash
arecord -D plughw:3,0 -f S16_LE -r 48000 -c 2 -d 5 -t wav test48k.wav
```

48 kHz captures frequencies up to 24 kHz, well above the 8 kHz limit of a 16 kHz sample rate, so it keeps the harmonics in cockatiel calls.

## Design

### Goals

1. Data Collection
  a. Recognize and record cockatiel vocalizations.
2. Data Analysis
  a. Basic classification to begin. Identify screams/screeches from other vocalizations. Basic frequency analysis to identify patterns in vocalizations.
  b. Advanced classification to identify specific vocalizations and their meanings.
3. Data Visualization
  a. Visualize data on a web accessible dashboard.

### Implementation

**Onboard**

Python script running on a Raspberry Pi with a ReSpeaker 2-Mics Pi HAT. The script will record audio, detect vocalizations, and send the data to the server.

**Server**

Visualization and analysis of the data will be done on a server. The server will receive the data from the Raspberry Pi, store it in a database, and provide a web interface for visualization and analysis.

## Todo

- [ ] Sample and label a dataset of cockatiel vocalizations.

## Journal

### 2026-11-20

- Got the ReSpeaker 2-Mics Pi HAT working with a Raspberry Pi 4B. The HAT is recognized as card 3 in `arecord -l`. The default settings produce near-silent recordings, so I had to configure the mixer in `alsamixer` to enable the input path and set appropriate gain levels. Recorded a test clip at 48 kHz, which captures me whistling.
- Loaded the [whistle clip](./notable-clips/whistle.wav) into Raven Lite and generated [a spectrogram](./assets/whistle.png). Took my first stab at labeling the clip, but this is fake data.
