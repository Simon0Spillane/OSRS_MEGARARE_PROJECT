## Data Collection (In Progress)

### Source
Price history comes from the [Weird Gloop](https://api.weirdgloop.org/) Exchange API
(`/exchange/history/osrs/all`), which provides historical Grand Exchange prices.

### Items Tracked

| # | Item              | Item ID | Color  |
|---|-------------------|---------|--------|
| 1 | Twisted bow       | 20997   | Green  |
| 2 | Scythe of Vitur   | 22486   | Red    |
| 3 | Tumeken's Shadow  | 27277   | Blue   |
| 4 | Obligator         | 34717   | Orange |

### Data File
- **File:** `<filename>`
- **Format:** `<CSV / JSON>`
- **Columns:** `<e.g. timestamp, id, price, volume>`
- **Date range:** `<start>` to `<end>`
- **Rows per item:** `<count>`

### Status
- [x] Pull price history for all four items
- [ ] Clean and validate (missing dates, gaps, zero-volume days)
- [ ] Plot full price history (log y-axis)
- [ ] Plot zoomed window around the Tombs of Amascut release
