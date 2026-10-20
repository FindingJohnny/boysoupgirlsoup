# Girl Soup, Boy Soup

A two-player guessing game: is it a girl soup or a boy soup?

- **Create a room**, then share the link with your partner. Each of you guesses on your own phone; the card flips once you've both picked.
- **Play on one phone** if you're sitting together.

It's a single static page (`index.html`), so any static host works. The two phones talk directly over WebRTC using [PeerJS](https://peerjs.com) and its free public matchmaking server, so there's no backend to run. The person who created the room needs to keep the page open while you play.

## License

All rights reserved. See [LICENSE](LICENSE).
