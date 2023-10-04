# this is a list for four file sessions.
# Update this list with your names
# Keep in mind that you also need to update the list symbol_used, noise_versions and titles
# all this lists need the same amount of elements
# please pay attention to spacebars. Replace them with underscore (_)
fileNames = [
    "emoTouch_aus_einschleichend_MIT_aufforderung",
    "emoTouch_pretest_ein_ausschleichend_MIT_aufforderung",
    "emoTouch_pretest_ein_ausschleichend_ohne_aufforderung",
    "emoTouch_aus_einschleichend_ohne_neu",
]

# you can update this ending if it doesn't fits your needs
# these are the default endings wich are added to all emotouch .csv-files
timeline_data_ending = "_timeline_data_v1.6.1"
session_metadata_ending = "_session_metadata_v1.6.1"
version_1_7_ending = "_version1.7_(100_ms)"

# This is a list of all soSci Survey Ids which you want to have in your results.
# You need to update this list for your needs
needed_ids = [
    441,
    442,
    447,
    453,
    475,
    477,
    486,
    487,
    490,
    494,
    498,
    503,
    520,
    524,
    530,
    531,
    532,
    534,
    535,
    538,
    539,
    545,
    547,
    550,
    552,
    560,
    565,
    569,
    571,
    574,
    575,
    576,
    584,
    585,
    593,
    595,
    611,
    615,
    616,
    621,
    622,
    635,
    659,
    664,
    667,
    676,
    677,
    681,
    688,
    693,
    700,
    701,
    705,
    721,
    726,
    728,
    746,
    748,
    756,
    761,
    766,
    767,
    770,
    773,
    780,
    781,
    785,
    788,
    798,
    808,
    811,
    812,
    814,
    823,
    839,
    845,
    847,
    859,
    866,
    867,
    868,
    878,
    880,
    883,
    887,
    889,
    890,
    891,
    893,
    906,
    907,
    912,
    913,
    917,
    931,
    937,
    948,
]

# this is a very specific case which you are generaly don't need.
# Just type False for the amount of your used files
symbol_used = [True, True, False, False]

# update for each file type your plot titles
titles = [
    "Versuch: aus- und einschleichendes Rauschen mit Aufforderung, ID: ",
    "Versuch: ein- und ausschleichendes Rauschen mit Aufforderung, ID: ",
    "Versuch: ein- und ausschleichendes Rauschen ohne Aufforderung, ID: ",
    "Versuch: aus- und einschleichendes Rauschen ohne Aufforderung, ID: ",
]

hystersis_title_single = [
    "Bewertungseingaben mit Aufforderung, \n aufgetragen gegenüber einer normierten aus-einschleichenden Rauschkurve.",
    "Bewertungseingaben mit Aufforderung, \n aufgetragen gegenüber einer normierten ein-ausschleichenden Rauschkurve.",
    "Bewertungseingaben ohne Aufforderung, \n aufgetragen gengegenüber einer normierten ein-ausschleichenden Rauschkurve.",
    "Bewertungseingaben ohne Aufforderung, \n aufgetragen gegenüber einer normierten aus-einschleichenden Rauschkurve.",
]

hystersis_title_mean = [
    "Gemittelte Bewertungseingaben mit Aufforderung, \n aufgetragen gegenüber einer normierten aus-einschleichenden Rauschkurve.",
    "Gemittelte Bewertungseingaben mit Aufforderung, \n aufgetragen gegenüber einer normierten ein-ausschleichenden Rauschkurve.",
    "Gemittelte Bewertungseingaben ohne Aufforderung, \n aufgetragen gegenüber einer normierten ein-ausschleichenden Rauschkurve.",
    "Gemittelte Bewertungseingaben ohne Aufforderung, \n aufgetragen gegenüber einer normierten aus-einschleichenden Rauschkurve.",
]

hystersis_title_compare = [
    "Vergleich zweier gemittelter Bewertungseingaben, \n aufgetragen gegenüber einer ein-ausschleichenden Rauschkurve",
    "Vergleich zweier gemittelter Bewertungseingaben, \n aufgetragen gegenüber einer aus-einschleichenden Rauschkurve",
]

mean_titles = [
    "Gemittelte Bewertungseingaben der aus-einschleichenden Rauschkurve mit Aufforderung",
    "Gemittelte Bewertungseingaben der ein-ausschleichenden Rauschkurve mit Aufforderung",
    "Gemittelte Bewertungseingaben der ein-ausschleichenden Rauschkurve ohne Aufforderung",
    "Gemittelte Bewertungseingaben der aus-einschleichenden Rauschkurve ohne Aufforderung",
]

mean_titles_cutted = [
    "Gemittelte und auf 68 Sekunden beschränkte \nBewertungseingaben der aus-einschleichenden Rauschkurve mit Aufforderung",
    "Gemittelte und auf 68 Sekunden beschränkte \nBewertungseingaben der ein-ausschleichenden Rauschkurve mit Aufforderung",
    "Gemittelte und auf 68 Sekunden beschränkte \nBewertungseingaben der ein-ausschleichenden Rauschkurve ohne Aufforderung",
    "Gemittelte und auf 68 Sekunden beschränkte \nBewertungseingaben der aus-einschleichenden Rauschkurve ohne Aufforderung",
]

mean_titles_difference = [
    "Differenz zwischen den gemittelte Bewertungseingaben \nund der aus-einschleichenden Rauschkurve mit Aufforderung",
    "Differenz zwischen den gmittelte Bewertungseingaben \nund der ein-ausschleichenden Rauschkurve mit Aufforderung",
    "Differenz zwischen den gemittelte Bewertungseingaben \nund der ein-ausschleichenden Rauschkurve ohne Aufforderung",
    "Differenz zwischen den gemittelte Bewertungseingaben \nund der aus-einschleichenden Rauschkurve ohne Aufforderung",
]

mean_title_compare = [
    "Vergleich zweier gemittelter Bewertungseingaben der ein-ausschleichenden Rauschkurve",
    "Vergleich zweier gemittelter Bewertungseingaben der aus-einschleichenden Rauschkurve",
]
