# Girl Soup, Boy Soup

A two-player guessing game: is it a girl soup or a boy soup?

- Each game deals 10 girl soups and 10 boy soups from a list of 186, each with a photo, a Wikipedia link and a recipe search. At the end you see every card and what you both picked.
- **Create a room**, then share the link with your partner. Each of you guesses on your own phone; the card flips once you've both picked.
- **Play on one phone** if you're sitting together.

It's a single static page (`index.html`), so any static host works. The two phones talk directly over WebRTC using [PeerJS](https://peerjs.com) and its free public matchmaking server, so there's no backend to run. The person who created the room needs to keep the page open while you play.

## Editing the soups

The list lives in `scripts/soups.json` (name, side, rank, the closest Wikipedia article, and a recipe search phrase). After changing it, run `python3 scripts/build_soups.py` to look up the photos and update `index.html`. Photos come from Wikimedia Commons via Wikipedia.

## License

All rights reserved. See [LICENSE](LICENSE).
