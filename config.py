settings = {

    "aoibounds": ( -118.377,34.0088,-118.347,34.0307),
    # "aoibounds": (-6.25989,53.3237,-6.25045,53.3285),
    #"systems": ["RES", "COM", "PREC", "ATRANS", "PTRANS", ],
    "systems": ["RES",],
    "outputdirectory": "output",
    "workingdirectory": "working",
    "osmdata": "https://gdh-data-sandbox.ams3.digitaloceanspaces.com/weogeo_j276494.zip",
    # "osmdata": "https://gdh-data-sandbox.ams3.digitaloceanspaces.com/weogeo_j273259.zip"
}

# Mapzen
# filekeys = {
#     "admin": "admin.geojson",
#     "aeroways": "aeroways.geojson",
#     "aminities": "aminities.geojson",
#     "buildings": "buildings.geojson",
#     "landusages": "landusages.geojson",
#     "roads": "roads.geojson",
#     "transportpoints": "transportpoints.geojson",
#     "waterareas": "waterareas.geojson",
#     "waterways": "waterways.geojson"##
# }

processchains = {
    "RES": {
        "red": {
            "files": [{
                "building": {
                    "type": "polygon",
                    "fields": {
                        "building": ['apartments', 'bungalow', 'bunglow', 'cabin', 'commercial;residential', 'house', 'residential', 'semi', 'semidetached_house'],

                    }
                }
            }]
        },
        "yellow": {
            "files": [{
                "natural": {
                    "type": "polygon",
                    "fields": {
                        "natural": ['water'],
                    },
                },
                # "building": {
                #     "type": "polygon",
                #     "fields": {
                #         "building": ['yes'],

                #     }
                # }
            }]
        },
        "green": {
            "files": [{
                "leisure": {
                    "type": "polygon",
                    "fields": {
                        "leisure": ['common', 'fitness_centre', 'garden', 'golf_course', 'marina', 'nature_reserve', 'park', 'picnic_table', 'pitch', 'playground', 'recreation_ground', 'slipway', 'sports_centre', 'stadium', 'swimming_pool', 'track'],

                    }
                }
            }, ]
        }
    },
    "COM": {
        "red": {
            "files": [{
                "building": {
                    "type": "polygon",
                    "fields": {
                        "building": ['commercial','yes'],
                    }
                }
            }, {
                "amenity": {
                    "type": "point",
                    "fields": {
                        "amenity": ['atm', 'bank', 'bar', 'bus_station', 'cafe', 'car_rental', 'car_wash', 'charging_station', 'childcare', 'cinema', 'clinic', 'dentist', 'doctors', 'marketplace', 'nightclub', 'pub', 'recycling', 'restaurant', 'theatre'],
                    }
                }
            }, {
                "shop": {
                    "type": "point",
                    "fields": {
                        "amenity": ['alcohol', 'bakery', 'beauty', 'beverages', 'bicycle', 'books', 'boutique', 'butcher', 'car', 'car_parts', 'car_repair', 'chemist', 'clothes', 'computer', 'confectionery', 'convenience', 'copyshop', 'cosmetics', 'deli', 'department_store', 'doityourself', 'dry_cleaning', 'electronics', 'florist', 'funeral_directors', 'furniture', 'garden_centre', 'gift', 'greengrocer', 'hairdresser', 'hardware', 'jewelry', 'kiosk', 'laundry', 'mall', 'mobile_phone', 'motorcycle', 'newsagent', 'optician', 'pet', 'shoes', 'sports', 'stationery', 'supermarket', 'toys', 'travel_agency', 'tyres', 'vacant', 'variety_store', 'yes', ],
                    }
                }
            }, ]
        },
        "yellow": {
            "files": [{
                "building": {
                    "type": "polygon",
                    "fields": {
                        "building": ['apartments', 'bungalow', 'bunglow', 'cabin', 'commercial;residential', 'house', 'residential', 'semi', 'semidetached_house'],
                    }
                }
            }, {
                "natural": {
                    "type": "polygon",
                    "fields": {
                        "natural": ['water'],
                    }
                }
            }]},
        "green": {
            "files": [{
                "leisure": {
                    "type": "polygon",
                    "fields": {
                        "leisure": ['common', 'fitness_centre', 'garden', 'golf_course', 'marina', 'nature_reserve', 'park', 'picnic_table', 'pitch', 'playground', 'recreation_ground', 'slipway', 'sports_centre', 'stadium', 'swimming_pool', 'track'],
                    }
                }
            }, ]
        }
    },
    "PREC": {
        "red": {
            "files": [{
                "leisure": {
                    "type": "polygon",
                    "fields": {
                        "leisure": ['common', 'fitness_centre', 'garden', 'golf_course', 'marina', 'nature_reserve', 'park', 'picnic_table', 'pitch', 'playground', 'recreation_ground', 'slipway', 'sports_centre', 'stadium', 'swimming_pool', 'track', 'swimming_pool', ],
                    }
                }
            }, ]
        },
        "yellow": {
            "files": [{
                "building": {
                    "type": "polygon",
                    "fields": {
                        "building": ['apartments', 'bungalow', 'bunglow', 'cabin', 'commercial;residential', 'house', 'residential', 'semi', 'semidetached_house'],
                    }
                }
            }, {
                "natural": {
                    "type": "polygon",
                    "fields": {
                        "natural": ['water'],
                    }
                }
            }]},
        "green": {
            "files": [{
                "amenity": {

                    "type": "polygon",
                    "fields": {
                        "amenity": ['community_centre', 'library', 'post_office', 'public_building', 'social_facility', 'theatre'],
                    }
                }
            }, ]
        }
    },
    "ATRANS": {
        "red": {
            "files": [{
                "highway": {
                    "type": "lines",
                    "fields": {
                        "highway": ['cycleway', 'footway', 'pedestrian', ],
                    }
                }
            }, ]
        },

        "yellow": {},
        "green": {
            "files": [{
                "highway": {

                    "type": "lines",
                    "fields": {
                        "highway": ['tertiary', 'primary',  'secondary'],
                    }
                }
            }, ]
        }
    },
    "PTRANS": {
        "red": {
            "files": [{
                "route": {
                    "type": "point",
                    "fields": {
                        "role": ['stop'],
                    }
                }
            }, ]
        },
        "yellow": {},
        "green": {
            "files": [{
                "highway": {
                    "type": "lines",
                    "fields": {
                        "highway": ['primary',  'secondary', 'tertiary'],
                    }
                }
            }, ]
        }
    },
    "COMFAC": {
        "red": {
            "files": [{
                "leisure": {
                    "type": "polygon",
                    "fields": {
                        "leisure": ['common', 'fitness_centre', 'garden', 'golf_course', 'marina', 'nature_reserve', 'park', 'picnic_table', 'pitch', 'playground', 'recreation_ground', 'slipway', 'sports_centre', 'stadium', 'swimming_pool', 'track'],

                    }
                }
            },]
        },
        "yellow": {},
        "green": {
            "files": [{
                "landuse": {
                    "type": "polygons",
                    "fields": {
                        "landuse": [ 'allotments','brownfield','farm','farmland','farmyard','forest','grass','greenfield','greenhouse_horticulture','meadow','military','orchard','plant_nursery','recreation_ground','village_green'],
                    }
                }
            }, ]
        }
    },
    "TOUR": {
        "red": {
            "files": [{
                "tourism": {
                    "type": "point",
                    "fields": {
                        "tourism": [ 'alpine_hut','artwork','attraction','camp_site','caravan_site','chalet','guest_house','hostel','hotel','information','motel','museum','picnic_site','viewpoint'],
                    }
                },
            }, ]
        },
        "yellow": {},
        "green": {
            "files": [{
                "historic": {
                    "type": "point",
                    "fields": {
                        "historic": [ 'yes','archaeological_site','building','castle','memorial','monument','ruins','tomb'],
                    }
                }
            }, ]
        }
    }
}
