Demo - Prrof of concept: Control a remove browser (inside Docker) streamed by WebRTC

## Compile new pipeline gst-rust
1 - `cargo build` in `./gst-rust`
2 - copy `./gst-rust/target/debug/gst-rust` in `./browser/files`


## Todo
- massive clean up
- dynamic resolution?
- improve keyboard & mouse events
- improve latency of the Gstreamer pipeline



Based from Centricular's demos: https://github.com/centricular/gstwebrtc-demos and Webrecorder's browsers: https://github.com/oldweb-today/browsers