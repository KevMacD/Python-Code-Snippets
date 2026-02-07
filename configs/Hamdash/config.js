// CUT START
var disableSetup = false; // Manually set to true to disable setup page menu option
var disableLdCfg = true;
var topBarCenterText = "VE7KVO";

// Grid layout desired
var layout_cols = 4;
var layout_rows = 2;

// Menu items
// Structure is as follows: HTML Color code, Option, target URL, scaling 1=Original Size, side (optional, nothing is Left, "R" is Right)
// The values are [color code, menu text, target link, scale factor, side],
// add new lines following the structure for extra menu options. The comma at the end is important!
var aURL = [];

// Feed items
// Structure is as follows: target URL
// The values are [target link]
var aRSS = [];

// Dashboard Tiles items
// Tile Structure is Title, Source URL
// To display a website on the tiles use "iframe|" keyword before the tile URL
// [Title, Source URL],
// the comma at the end is important!
var aIMG = [
  [
    "",
    "https://cdn.star.nesdis.noaa.gov/GOES19/ABI/SECTOR/can/AirMass/GOES19-CAN-AirMass-1125x560.gif"
  ],
  [
    "",
    "https://cdn.star.nesdis.noaa.gov/GOES18/ABI/SECTOR/sea/GEOCOLOR/GOES18-SEA-GEOCOLOR-600x600.gif"
  ],
  [
    "",
    "https://cdn.star.nesdis.noaa.gov/GOES16/GLM/SECTOR/can/EXTENT3/GOES16-CAN-EXTENT3-1125x560.gif"
  ],
  [
    "",
    "iframe|https://api.wo-cloud.com/content/widget/?geoObjectKey=8779322&language=en&region=US&timeFormat=HH:mm&windUnit=mph&systemOfMeasurement=metric&temperatureUnit=celsius"
  ],
  [
    "",
    "https://cdn.star.nesdis.noaa.gov/GOES19/SUVI/FD/Fe171/GOES19-SUVI-Fe171-600x600.gif"
  ],
  [
    "",
    "https://services.swpc.noaa.gov/images/animations/ovation/north/latest.jpg"
  ],
  [
    "",
    "https://services.swpc.noaa.gov/images/animations/ovation/south/latest.jpg"
  ],
  [
    "",
    "https://www.hamqsl.com/solar101vhf.php",
    "https://www.hamqsl.com/solar100sc.php",
    "https://www.hamqsl.com/solarpich.php"
  ]
];

// Image rotation intervals in milliseconds per tile - If the line below is commented, tiles will be rotated every 5000 milliseconds (5s)
var tileDelay = [
  10000,
  10000,
  10000,
  10000,
  5000,
  5000,
  5000,
  5000
];

// CUT END