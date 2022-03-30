from django.db import models

from config.models import BaseModel


# === plant 앱에 포함 ===
class PlantCategory(BaseModel):
    category = models.CharField(max_length=45)


class Plant(BaseModel):
    plant_category_id = models.ForeignKey(
        PlantCategory, on_delete=models.CASCADE, related_name="plant", db_column="plant_category_id"
    )
    main_name = botanical_name = models.CharField(max_length=100, null=True, blank=True)
    image = models.CharField(max_length=256, null=True, blank=True)

    botanical_name = models.CharField(max_length=100, null=True, blank=True)
    english_name = models.CharField(max_length=150, null=True, blank=True)
    general_name = models.CharField(max_length=100, null=True, blank=True)
    type_name = models.CharField(max_length=100, null=True, blank=True)
    origin = models.CharField(max_length=100, null=True, blank=True)
    advise_info = models.CharField(max_length=100, null=True, blank=True)
    image_link = models.CharField(max_length=256, null=True, blank=True)
    height_info = models.IntegerField(null=True, blank=True)
    width_info = models.IntegerField(null=True, blank=True)
    leaftype_info = models.CharField(max_length=100, null=True, blank=True)

    # smell_info = models.CharField(max_length=100)
    toxic_info = models.CharField(max_length=100, null=True, blank=True)
    breeding_info = models.CharField(max_length=100, null=True, blank=True)
    extraperiod_info = models.CharField(max_length=100, null=True, blank=True)
    grow_level = models.CharField(max_length=100, null=True, blank=True)
    growth_speed = models.CharField(max_length=100, null=True, blank=True)
    growth_temp = models.CharField(max_length=100, null=True, blank=True)
    lowest_temp = models.CharField(max_length=100, null=True, blank=True)
    humidity = models.CharField(max_length=100, null=True, blank=True)
    fertilizer_info = models.CharField(max_length=100, null=True, blank=True)

    soil_info = models.CharField(max_length=100, null=True, blank=True)
    water_spring = models.CharField(max_length=100, null=True, blank=True)
    water_summer = models.CharField(max_length=100, null=True, blank=True)
    water_fall = models.CharField(max_length=100, null=True, blank=True)
    water_winter = models.CharField(max_length=100, null=True, blank=True)
    insect_info = models.CharField(max_length=256, null=True, blank=True)
    extragrow_info = models.CharField(max_length=2000, null=True, blank=True)
    functional_info = models.CharField(max_length=2000, null=True, blank=True)
    # potsize_big = models.IntegerField(null=True, blank=True)
    # potsize_mid = models.IntegerField(null=True, blank=True)
    #
    # potsize_small = models.IntegerField(null=True, blank=True)
    # width_big = models.IntegerField(null=True, blank=True)
    # width_mid = models.IntegerField(null=True, blank=True)
    # width_small = models.IntegerField(null=True, blank=True)
    # length_big = models.IntegerField(null=True, blank=True)
    # length_mid = models.IntegerField(null=True, blank=True)
    # length_small = models.IntegerField(null=True, blank=True)
    # heigt_big = models.IntegerField(null=True, blank=True)
    # heigt_mid = models.IntegerField(null=True, blank=True)
    # heigt_small = models.IntegerField(null=True, blank=True)
    #
    # volume_big = models.IntegerField(null=True, blank=True)
    # volume_mid = models.IntegerField(null=True, blank=True)
    # volume_small = models.IntegerField(null=True, blank=True)
    # price_big = models.IntegerField(null=True, blank=True)
    # price_mid = models.IntegerField(null=True, blank=True)
    # price_small = models.IntegerField(null=True, blank=True)
    care_need = models.CharField(max_length=100, null=True, blank=True)
    type = models.CharField(max_length=100, null=True, blank=True)
    growth_type = models.CharField(max_length=100, null=True, blank=True)
    indoor_garden = models.CharField(max_length=100, null=True, blank=True)

    ecology = models.CharField(max_length=100, null=True, blank=True)
    leaf_pattern = models.CharField(max_length=100, null=True, blank=True)
    leaf_color = models.CharField(max_length=100, null=True, blank=True)
    flower_season = models.CharField(max_length=100, null=True, blank=True)
    flower_color = models.CharField(max_length=100, null=True, blank=True)
    fluit_season = models.CharField(max_length=100, null=True, blank=True)
    fluit_color = models.CharField(max_length=100, null=True, blank=True)
    breeding_way = models.CharField(max_length=100, null=True, blank=True)
    lux = models.CharField(max_length=100, null=True, blank=True)
    location = models.CharField(max_length=256, null=True, blank=True)

    # insect = models.CharField(max_length=100, null=True, blank=True)
