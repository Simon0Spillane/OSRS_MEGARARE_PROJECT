# OSRS_MEGARARE_PROJECT
Information Science Project on Old School Runescape Items  
by Simon Spillane

## Question: 
Data analysis project looking at the historical price and volume of OLD School Runescape (OSRS) Megarares using data from OSRS Wiki API. The goal is to compare historical market trends with game updates to discover correlations between price/volume fluctuations over time. 

## Data: 

Using the [Weird Gloop](https://runescape.wiki/w/Application_programming_interface) Grand Exchange history API.

- **Source:** Weird Gloop exchange history endpoint (`/exchange/history/osrs/all`)
- **Snapshot:** data is roughly one week old
- **Coverage:** historic price data for all four items
- **In progress:** a cleaned table of game updates that mention each item
  
So far, each item's plot includes a vertical line marking when others were added to the game. The next step is a cleaned list of every game update that mentions these items, so price changes can be tied to updates.

## Items

| Item | Item ID | Added to game |
|------|---------|---------------|
| Twisted bow | `20997` | <!-- TODO --> |
| Scythe of Vitur | `22486` | <!-- TODO --> |
| Tumeken's Shadow | `27277` | <!-- TODO --> |
| Obligator | `34717` | <!-- TODO --> |


## Methods

- **Python** with `requests` for API calls and `pandas` for cleaning and analysis
- Data from the Reldo Wiki Archive
- Prices plotted on line graphs with indicator for game updates
- Eventually there will be one color per item for easy comparison

## Visualizations

TBD

## Findings:  
