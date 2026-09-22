# Supply identification photos

These are supplier/product reference photos, not photographs of delivered
Stauffer inventory. The public catalog records each original image URL, source
page, attribution, check date, dimensions, and identification caption. Images
are stored locally and have not been altered. Attribution is displayed beside
each photo and in the enlarged view; original owners retain their rights.

`Order-list product` means the source matches a listed ASIN, not that delivery
or suitability has been confirmed. `Equivalent example` means a different
supplier/product illustrates the general appearance. `Manufacturer reference`
and `Supplier reference` likewise do not establish the delivered revision,
connector pinout, or approved power arrangement.

To replace a reference with a verified classroom photograph:

1. Add the photo here with a descriptive filename. Avoid student faces or names.
2. Update its existing entry in `catalog.json`, including `src`, original
   dimensions, alt text, caption, source, and kind. Keep the stable `id`.
3. Run `python scripts/build_supply_photos.py`, then
   `python scripts/check_curriculum.py`.
4. Check the collapsed panel, expanded grid, photo viewer, and phone layout.

Panels use native details/summary and lazy-loaded image links. JavaScript adds
one accessible dialog per page; direct image links remain usable without it.
The photo panels and dialog are hidden during printing so the existing lesson
and clipboard layouts stay compact.
