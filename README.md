# Squawk Box

A platform dedicated to detecting, aggregating, and classifying my pet cockatiel's vocalizations.

## Setup

https://wiki.seeedstudio.com/respeaker_2_mics_pi_hat_raspberry_v2/

## Design

### Goals

1. Data Collection
  a. Recognize and record cockatiel vocalizations.
2. Data Analysis
  a. Basic classification to begin. Identify screams/screeches from other vocalizations. Basic frequency analysis to identify patterns in vocalizations.
  b. Advanced classification to identify specific vocalizations and their meanings.
3. Data Visualiztion
  a. Visualize data on a web accessible dashboard.

### Implementation

**Onboard**

Python script running on a Raspberry Pi with a ReSpeaker 2-Mics Pi HAT. The script will record audio, detect vocalizations, and send the data to the server.

**Server**

Visualization and analysis of the data will be done on a server. The server will receive the data from the Raspberry Pi, store it in a database, and provide a web interface for visualization and analysis.
