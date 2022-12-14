"""
COUNTRY_CHOICES contains the available countries in which the customer can shop.
COUNTY_CHOICES contains all the Greek counties.
QUANTITY_CHOICES contains a list of tuples from 1-49.
PAYMENT_CHOICES contains the [ayment methods supported, i.e. cash and card.
"""

COUNTRY_CHOICES = (
  ('Ελλάδα', 'Ελλάδα'),
)

COUNTY_CHOICES = (
  ('Νομός Αιτωλοακαρνανίας', 'Νομός Αιτωλοακαρνανίας'),
  ('Νομός Αργολίδας', 'Νομός Αργολίδας'),
  ('Νομός Αρκαδίας', 'Νομός Αρκαδίας'),
  ('Νομός Άρτας', 'Νομός Άρτας'),
  ('Νομός Αχαίας', 'Νομός Αχαίας'),
  ('Νομός Αττικής', 'Νομός Αττικής'),
  ('Νομός Βοιωτίας', 'Νομός Βοιωτίας'),
  ('Νομός Γρεβενών', 'Νομός Γρεβενών'),
  ('Νομός Δράμας', 'Νομός Δράμας'),
  ('Νομός Δωδεκανήσου', 'Νομός Δωδεκανήσου'),
  ('Νομός Έβρου', 'Νομός Έβρου'),
  ('Νομός Ευβοίας', 'Νομός Ευβοίας'),
  ('Νομός Ευρυτανίας', 'Νομός Ευρυτανίας'),
  ('Νομός Ζακύνθου', 'Νομός Ζακύνθου'),
  ('Νομός Ηλείας', 'Νομός Ηλείας'),
  ('Νομός Ημαθίας', 'Νομός Ημαθίας'),
  ('Νομός Ηρακλείου', 'Νομός Ηρακλείου'),
  ('Νομός Θεσπρωτίας', 'Νομός Θεσπρωτίας'),
  ('Νομός Θεσσαλονίκης', 'Νομός Θεσσαλονίκης'),
  ('Νομός Ιωαννίνων', 'Νομός Ιωαννίνων'),
  ('Νομός Καβάλας', 'Νομός Καβάλας'),
  ('Νομός Καρδίτσας', 'Νομός Καρδίτσας'),
  ('Νομός Καστοριάς', 'Νομός Καστοριάς'),
  ('Νομός Κέρκυρας', 'Νομός Κέρκυρας'),
  ('Νομός Κεφαλλονιάς', 'Νομός Κεφαλλονιάς'),
  ('Νομός Κιλκίς', 'Νομός Κιλκίς'),
  ('Νομός Κοζάνης', 'Νομός Κοζάνης'),
  ('Νομός Κορινθίας', 'Νομός Κορινθίας'),
  ('Νομός Κυκλάδων', 'Νομός Κυκλάδων'),
  ('Νομός Λακωνίας', 'Νομός Λακωνίας'),
  ('Νομός Λάρισας', 'Νομός Λάρισας'),
  ('Νομός Λασιθίου', 'Νομός Λασιθίου'),
  ('Νομός Λέσβου', 'Νομός Λέσβου'),
  ('Νομός Λευκάδας', 'Νομός Λευκάδας'),
  ('Νομός Μαγνησίας', 'Νομός Μαγνησίας'),
  ('Νομός Μεσσηνίας', 'Νομός Μεσσηνίας'),
  ('Νομός Ξάνθης', 'Νομός Ξάνθης'),
  ('Νομός Πέλλας', 'Νομός Πέλλας'),
  ('Νομός Πιερίας', 'Νομός Πιερίας'),
  ('Νομός Πρέβεζας', 'Νομός Πρέβεζας'),
  ('Νομός Ρεθύμνου', 'Νομός Ρεθύμνου'),
  ('Νομός Ροδόπης', 'Νομός Ροδόπης'),
  ('Νομός Σάμου', 'Νομός Σάμου'),
  ('Νομός Σερρών', 'Νομός Σερρών'),
  ('Νομός Τρικάλων', 'Νομός Τρικάλων'),
  ('Νομός Φθιώτιδας', 'Νομός Φθιώτιδας'),
  ('Νομός Φλώρινας', 'Νομός Φλώρινας'),
  ('Νομός Φωκίδας', 'Νομός Φωκίδας'),
  ('Νομός Χαλκιδικής', 'Νομός Χαλκιδικής'),
  ('Νομός Χανίων', 'Νομός Χανίων'),
  ('Νομός Χίου', 'Νομός Χίου'),
)

QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 50)]

PAYMENT_CHOICES = (
    ('Αντικαταβολή', 'Αντικαταβολή'),
    ('Πληρωμή με κάρτα', 'Πληρωμή με κάρτα'),
  )
