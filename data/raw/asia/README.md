# Raw transcriptions for Asian peers

- `mlit_yardstick_tokyo.csv`: MLIT 鉄道統計年報, yardstick table (JR旅客会社、大手民鉄及び地下鉄事業者の基準単価及び基準コストの算定に係るデータ一覧), section 地下鉄事業者, columns 東京地下鉄 and 東京都, FY2015-FY2023. One row per printed item. Money in thousand yen as printed. Sources `mlit_yardstick_fy<year>`. Read from the PDF text layer; `scripts/build_tokyo_inputs.py` checks three printed sum identities for every year and operator before writing rows. Toei's 諸税 (taxes) for FY2019-FY2023 could not be split cleanly from the text and was set from the identity 合計 + 減価償却費 + 諸税 = 営業費計 (0, or ¥1,000 in FY2023).
- `mtr_hk.py`: MTR Ten-Year Statistics (Annual Report 2025) and the Hong Kong transport lines of the consolidated profit and loss account from the results announcements, 2016-2025.
