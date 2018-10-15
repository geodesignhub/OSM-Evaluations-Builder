settings = {

    "aoifile": "https://gdh-data.ams3.digitaloceanspaces.com/boun.geojson",
    # "systems": ["RES", "COM", "PREC", "ATRANS", "PTRANS", ],
    "systems": ["RES",],
    "outputdirectory": "output",
    "workingdirectory": "working",
    "osmdata": "/Users/hrishiballal/Desktop/mamo.geojson",
}


processchains = {
    "RES": {
        "red": {
            "files": [{
                "polygons": {
                    "fields": {
                        "building": ['apartments', 'bungalow', 'bunglow', 'cabin', 'commercial;residential', 'house', 'residential', 'semi', 'semidetached_house'],
                        

                    }
                }
            }]
        },
        "yellow": {
            "files": [{
                "polygons": {
                    "fields": {
                        "natural": ['water'],
                        # "building": ['yes'],
                    },
                },
            }]
        },
        "green": {
            "files": [{
                "polygons": {
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
                "polygons": {
                    "fields": {
                        "building": ['commercial','yes'],
                    }
                }
            }, {
                "points": {
                    "fields": {
                        "amenity": ['atm', 'bank', 'bar', 'bus_station', 'cafe', 'car_rental', 'car_wash', 'charging_station', 'childcare', 'cinema', 'clinic', 'dentist', 'doctors', 'marketplace', 'nightclub', 'pub', 'recycling', 'restaurant', 'theatre'],
                    }
                }
            }, {
                "points": {
                    "fields": {
                        "amenity": ['alcohol', 'bakery', 'beauty', 'beverages', 'bicycle', 'books', 'boutique', 'butcher', 'car', 'car_parts', 'car_repair', 'chemist', 'clothes', 'computer', 'confectionery', 'convenience', 'copyshop', 'cosmetics', 'deli', 'department_store', 'doityourself', 'dry_cleaning', 'electronics', 'florist', 'funeral_directors', 'furniture', 'garden_centre', 'gift', 'greengrocer', 'hairdresser', 'hardware', 'jewelry', 'kiosk', 'laundry', 'mall', 'mobile_phone', 'motorcycle', 'newsagent', 'optician', 'pet', 'shoes', 'sports', 'stationery', 'supermarket', 'toys', 'travel_agency', 'tyres', 'vacant', 'variety_store', 'yes', ],
                    }
                }
            }, ]
        },
        "yellow": {
            "files": [{
                "polygons": {
                    "fields": {
                        "building": ['apartments', 'bungalow', 'bunglow', 'cabin', 'commercial;residential', 'house', 'residential', 'semi', 'semidetached_house'],
                    }
                }
            }, {
                "polygons": {
                    "fields": {
                        "natural": ['water'],
                    }
                }
            }]},
        "green": {
            "files": [{
                "lines": {
                    "fields": {
                        "highway": ['tertiary', 'primary',  'secondary'],
                    }
                }
            },{
                "polygons": {
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
                "polygons": {
                    "fields": {
                        "leisure": ['common', 'fitness_centre', 'garden', 'golf_course', 'marina', 'nature_reserve', 'park', 'picnic_table', 'pitch', 'playground', 'recreation_ground', 'slipway', 'sports_centre', 'stadium', 'swimming_pool', 'track', 'swimming_pool', ],
                    }
                }
            }, ]
        },
        "yellow": {
            "files": [{
                "polygons": {
                    "fields": {
                        "building": ['apartments', 'bungalow', 'bunglow', 'cabin', 'commercial;residential', 'house', 'residential', 'semi', 'semidetached_house'],
                        "building": ['yes'],
                    }
                }
            }, {
                "polygons": {
                    "fields": {
                        "natural": ['water'],
                    }
                }
            }]},
        "green": {
            "files": [{
                "polygons": {
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
                "lines": {
                    "fields": {
                        "highway": ['cycleway', 'footway', 'pedestrian', ],
                    }
                }
            }, ]
        },

        "yellow": {},
        "green": {
            "files": [{
                "lines": {
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
                "points": {
                    "fields": {
                        "role": ['stop'],
                    }
                }
            }, ]
        },
        "yellow": {},
        "green": {
            "files": [{
                "lines": {
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
                "polygons": {
                    "fields": {
                        "leisure": ['common', 'fitness_centre', 'garden', 'golf_course', 'marina', 'nature_reserve', 'park', 'picnic_table', 'pitch', 'playground', 'recreation_ground', 'slipway', 'sports_centre', 'stadium', 'swimming_pool', 'track'],

                    }
                }
            },]
        },
        "yellow": {},
        "green": {
            "files": [{
                "polygons": {
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
                "points": {
                    "fields": {
                        "tourism": [ 'alpine_hut','artwork','attraction','camp_site','caravan_site','chalet','guest_house','hostel','hotel','information','motel','museum','picnic_site','viewpoint'],
                    }
                },
            }, ]
        },
        "yellow": {},
        "green": {
            "files": [{
                "points": {
                    "fields": {
                        "historic": [ 'yes','archaeological_site','building','castle','memorial','monument','ruins','tomb'],
                    }
                }
            }, ]
        }
    }
}
