from django.db import models
from django.utils.timezone import now


# Create your models here.
class CarMake(models.Model):
    """
    Django model representing a car manufacturer or brand.

    Attributes:
        name (CharField): A character field with a maximum length of 100 characters, representing the name of the car manufacturer or brand.
        description (TextField): A text field, allowing for a more detailed description of the car manufacturer or brand.
        created_at (DateTimeField): A date-time field that automatically records the date and time when the CarMake object is created.
        updated_at (DateTimeField): A date-time field that automatically records the date and time when the CarMake object is last updated.

    Behavior:
        The save method is overridden to ensure that the updated_at field is always updated with the current date and time whenever the CarMake object is saved or updated.
        The __str__ method is defined to return the name of the car manufacturer, making it easier to represent CarMake objects as strings, for example, in admin interfaces or debugging messages.
    """
    name = models.CharField(max_length=100)
    description = models.TextField()

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        return super(CarMake, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class CarModel(models.Model):
    """
    Django model representing a car model.

    Attributes:
        car_make (ForeignKey): A Many-to-One relationship field, linking each car model to a specific car make. When a car make is deleted, all related car models are also deleted (on_delete=models.CASCADE).
        name (CharField): A character field with a maximum length of 100 characters, representing the name of the car model.
        dealer_id (CharField): A character field with a maximum length of 100 characters, used to reference a dealer.
        car_type (CharField): A character field with a maximum length of 10 characters, providing limited choices (Sedan, SUV, Wagon) for the type of the car model.
        year (DateField): A date field representing the year of the car model.

    Date and Time Fields:
        created_at (DateTimeField): A date-time field that records the date and time when the CarModel object is created. It has a default value of the current timestamp.
        updated_at (DateTimeField): A date-time field that records the date and time when the CarModel object is last updated. It has a default value of the current timestamp.

    Behavior:
        The save method is overridden to ensure that the updated_at field is always updated with the current date and time whenever the CarModel object is saved or updated.
        The __str__ method is defined to provide a human-readable representation of the CarModel object. It returns a string containing the name of the car make associated with the model followed by the name of the car model itself.
    """
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    dealer_id = models.CharField(max_length=100)
    SEDAN = 'Sedan'
    SUV = 'SUV'
    WAGON = 'Wagon'
    CAR_TYPE_CHOICES = [
        (SEDAN, 'Sedan'),
        (SUV, 'SUV'),
        (WAGON, 'Wagon'),
        # Add more choices as needed
    ]
    car_type = models.CharField(max_length=10, choices=CAR_TYPE_CHOICES, default=SEDAN)
    year = models.DateField()

    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(default=now)

    def save(self, *args, **kwargs):
        self.updated_at = now()
        return super(CarModel, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.car_make.name} - {self.name}"

class CarDealer:

    """
    Fields:
        address: A character field representing the address of the car dealership.
        city: A character field representing the city where the car dealership is located.
        full_name: A character field with a maximum length of 100 characters, representing the full name of the car dealership.
        id: An identifier field representing the unique ID of the car dealership.
        lat: A floating-point field representing the latitude coordinate of the car dealership's location.
        long: A floating-point field representing the longitude coordinate of the car dealership's location.
        short_name: A character field with a maximum length of 100 characters, representing the short name or abbreviation of the car dealership.
        st: A character field representing the state where the car dealership is located.
        zip: A character field representing the zip code of the car dealership's location.

    Behavior:
        The __str__ method is defined to provide a human-readable representation of the CarDealer object. It returns a string containing the full name of the car dealership.
    """

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        self.address = address
        self.city = city
        self.full_name = full_name
        self.id = id
        self.lat = lat
        self.long = long
        self.short_name = short_name
        self.st = st
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year, sentiment, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.purchase_date = purchase_date
        self.car_make = car_make
        self.car_model = car_model
        self.car_year = car_year
        self.sentiment = sentiment
        self.id = id

    def __str__(self):
        return "Review: " + self.review +" Sentiment: " + self.sentiment
