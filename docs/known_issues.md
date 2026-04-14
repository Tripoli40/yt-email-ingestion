# Known Issues

- Some YouTube formats emit PO-token warnings or require extra site-specific handling upstream in `yt-dlp`
- TikTok extraction may depend on additional impersonation or JavaScript runtime support on the host
- Large downloads can overlap the next timer interval because the timer fires every 2 minutes
- There is no duplicate detection or persistent state tracking
- HTML-only emails may be missed because URL extraction currently reads `text/plain` parts and does not parse HTML bodies
