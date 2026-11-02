# Unit artwork

48 decorative banners, exported as WebP at 1800 and 960 pixels wide.
The 1800px version is lossless (identical decoded RGB pixels to the original PNG).
The 960px version uses quality 94. Both preserve the original 15:4 proportions.
On mobile a left-aligned 5:2 frame displays the illustrated left two-thirds,
trimming the empty navy right third without cropping the top or bottom.
The title, content counts and buttons sit below it on white. Student completion
uses a slim bar; the desktop ring and guest placeholder are hidden on mobile.
Responsive `sizes` accounts for the 1.5x source width required by this right-edge crop.
A mild CSS contrast/saturation correction improves the supplied soft artwork's
perceived clarity; the source files themselves remain unchanged. Desktop uses a matching 15:4 card with a subtle
edge overlay behind controls, leaving the centre of the illustration clear.
`UnitHeader` requests only the selected unit's image, using `srcset` for responsive sizing.
PNG originals remain outside the repository. Images contain no UI text or controls.

To regenerate (Python with Pillow):

```powershell
python frontend/scripts/convert-unit-backgrounds.py "PATH_TO_ORIGINAL_PNG_FOLDER"
```

Mapping follows the supplied `unit_01` through `unit_48` numbers. The supplied
`unit_09_travel.png` and `unit_10_shopping.png` names differ from the application's
unit 9 (shopping) and unit 10 (weather); their supplied numerical order is preserved.
