shelves = {
    "S1": {
        "type": "Checkout Display",
        "capacity_kg": 8,
        "refrigerated": False,
        "hazardous": False,
        "high_visibility": True,  
        "lower_shelf": False,     
        "secure": False           
    },
    "S2": {
        "type": "Lower Shelf",
        "capacity_kg": 25,
        "refrigerated": False,
        "hazardous": False,
        "high_visibility": False,
        "lower_shelf": True,      
        "secure": False
    },
    "S4": {
        "type": "Eye-Level Shelf",
        "capacity_kg": 15,
        "refrigerated": False,
        "hazardous": False,
        "high_visibility": True,  
        "lower_shelf": False,
        "secure": False
    },
    "S5": {
        "type": "General Aisle Shelf",
        "capacity_kg": 20,
        "refrigerated": False,
        "hazardous": False,
        "high_visibility": False,
        "lower_shelf": False,
        "secure": False
    },
    "R1": {
        "type": "Refrigerator Zone 1",
        "capacity_kg": 20,
        "refrigerated": True,    
        "hazardous": False,
        "high_visibility": False,
        "lower_shelf": False,
        "secure": False
    },
    "R2": {
        "type": "Refrigerator Zone 2",
        "capacity_kg": 15,
        "refrigerated": True,    
        "hazardous": False,
        "high_visibility": False,
        "lower_shelf": False,
        "secure": False
    },
    "R3": {
        "type": "Refrigerator Zone 3",
        "capacity_kg": 25,
        "refrigerated": True,    
        "hazardous": False,
        "high_visibility": False,
        "lower_shelf": False,
        "secure": False
    },
    "H1": {
        "type": "Hazardous Item Zone 1",
        "capacity_kg": 10,
        "refrigerated": False,
        "hazardous": True,       
        "high_visibility": False,
        "lower_shelf": False,
        "secure": True            
    },
    "H2": {
        "type": "Hazardous Item Zone 2",
        "capacity_kg": 12,
        "refrigerated": False,
        "hazardous": True,       
        "high_visibility": False,
        "lower_shelf": False,
        "secure": True            
    }
}

products = [
    {
        "id": 0,
        "name": "Milk",
        "weight_kg": 5,
        "category": "Dairy",
        "perishable": True,      
        "hazardous": False,
        "high_demand": True,     
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 1,
        "name": "Rice Bag",
        "weight_kg": 10,
        "category": "Grains",
        "perishable": False,
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 2,
        "name": "Frozen Nuggets",
        "weight_kg": 5,
        "category": "Frozen",
        "perishable": True,      
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 3,
        "name": "Cereal",
        "weight_kg": 3,
        "category": "Breakfast",
        "perishable": False,
        "hazardous": False,
        "high_demand": True,     
        "discounted": True,      
        "high_theft": False
    },
    {
        "id": 4,
        "name": "Pasta",
        "weight_kg": 2,
        "category": "Grains",
        "perishable": False,
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 5,
        "name": "Pasta Sauce",
        "weight_kg": 3,
        "category": "Condiments",
        "perishable": False,
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 6,
        "name": "Detergent",
        "weight_kg": 4,
        "category": "Cleaning",
        "perishable": False,
        "hazardous": True,        
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 7,
        "name": "Glass Cleaner",
        "weight_kg": 5,
        "category": "Cleaning",
        "perishable": False,
        "hazardous": True,        
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 8,
        "name": "Ice Cream",
        "weight_kg": 4,
        "category": "Frozen",
        "perishable": True,      
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 9,
        "name": "Yogurt",
        "weight_kg": 2,
        "category": "Dairy",
        "perishable": True,      
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 10,
        "name": "Bleach",
        "weight_kg": 6,
        "category": "Cleaning",
        "perishable": False,
        "hazardous": True,        
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 11,
        "name": "Bread",
        "weight_kg": 1,
        "category": "Bakery",
        "perishable": False,
        "hazardous": False,
        "high_demand": True,     
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 12,
        "name": "Cheese",
        "weight_kg": 3,
        "category": "Dairy",
        "perishable": True,      
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 13,
        "name": "Chicken Breast",
        "weight_kg": 7,
        "category": "Meat",
        "perishable": True,      
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 14,
        "name": "Tomato Sauce",
        "weight_kg": 2,
        "category": "Condiments",
        "perishable": False,
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 15,
        "name": "Coffee",
        "weight_kg": 1,
        "category": "Beverages",
        "perishable": False,
        "hazardous": False,
        "high_demand": True,     
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 16,
        "name": "Sugar",
        "weight_kg": 3,
        "category": "Baking",
        "perishable": False,
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 17,
        "name": "Flour",
        "weight_kg": 5,
        "category": "Baking",
        "perishable": False,
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 18,
        "name": "Butter",
        "weight_kg": 2,
        "category": "Dairy",
        "perishable": True,      
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    },
    {
        "id": 19,
        "name": "Eggs",
        "weight_kg": 3,
        "category": "Dairy",
        "perishable": True,      
        "hazardous": False,
        "high_demand": False,
        "discounted": False,
        "high_theft": False
    }
]

complementary_pairs = [
    (4, 5),   # Pasta and Pasta Sauce
    (15, 16), # Coffee and Sugar
    (17, 18), # Flour and Butter
    (12, 19)  # Cheese and Eggs
]









# # Define shelves with their attributes
# shelves = {
#     "S1": {
#         "type": "Checkout Display",
#         "capacity_kg": 8,
#         "refrigerated": False,
#         "hazardous": False,
#         "high_visibility": True,  
#         "lower_shelf": False,     
#         "secure": False           
#     },
#     "S2": {
#         "type": "Lower Shelf",
#         "capacity_kg": 25,
#         "refrigerated": False,
#         "hazardous": False,
#         "high_visibility": False,
#         "lower_shelf": True,      
#         "secure": False
#     },
#     "S4": {
#         "type": "Eye-Level Shelf",
#         "capacity_kg": 15,
#         "refrigerated": False,
#         "hazardous": False,
#         "high_visibility": True,  
#         "lower_shelf": False,
#         "secure": False
#     },
#     "S5": {
#         "type": "General Aisle Shelf",
#         "capacity_kg": 20,
#         "refrigerated": False,
#         "hazardous": False,
#         "high_visibility": False,
#         "lower_shelf": False,
#         "secure": False
#     },
#     "R1": {
#         "type": "Refrigerator Zone",
#         "capacity_kg": 20,
#         "refrigerated": True,    
#         "hazardous": False,
#         "high_visibility": False,
#         "lower_shelf": False,
#         "secure": False
#     },
#     "H1": {
#         "type": "Hazardous Item Zone",
#         "capacity_kg": 10,
#         "refrigerated": False,
#         "hazardous": True,       
#         "high_visibility": False,
#         "lower_shelf": False,
#         "secure": True            
#     }
# }

# products = [
#     {
#         "id": 0,
#         "name": "Milk",
#         "weight_kg": 5,
#         "category": "Dairy",
#         "perishable": True,      
#         "hazardous": False,
#         "high_demand": True,     
#         "discounted": False,
#         "high_theft": False
#     },
#     {
#         "id": 1,
#         "name": "Rice Bag",
#         "weight_kg": 10,
#         "category": "Grains",
#         "perishable": False,
#         "hazardous": False,
#         "high_demand": False,
#         "discounted": False,
#         "high_theft": False
#     },
#     {
#         "id": 2,
#         "name": "Frozen Nuggets",
#         "weight_kg": 5,
#         "category": "Frozen",
#         "perishable": True,      
#         "hazardous": False,
#         "high_demand": False,
#         "discounted": False,
#         "high_theft": False
#     },
#     {
#         "id": 3,
#         "name": "Cereal",
#         "weight_kg": 3,
#         "category": "Breakfast",
#         "perishable": False,
#         "hazardous": False,
#         "high_demand": True,     
#         "discounted": True,      
#         "high_theft": False
#     },
#     {
#         "id": 4,
#         "name": "Pasta",
#         "weight_kg": 2,
#         "category": "Grains",
#         "perishable": False,
#         "hazardous": False,
#         "high_demand": False,
#         "discounted": False,
#         "high_theft": False
#     },
#     {
#         "id": 5,
#         "name": "Pasta Sauce",
#         "weight_kg": 3,
#         "category": "Condiments",
#         "perishable": False,
#         "hazardous": False,
#         "high_demand": False,
#         "discounted": False,
#         "high_theft": False
#     },
#     {
#         "id": 6,
#         "name": "Detergent",
#         "weight_kg": 4,
#         "category": "Cleaning",
#         "perishable": False,
#         "hazardous": True,        
#         "high_demand": False,
#         "discounted": False,
#         "high_theft": False
#     },
#     {
#         "id": 7,
#         "name": "Glass Cleaner",
#         "weight_kg": 5,
#         "category": "Cleaning",
#         "perishable": False,
#         "hazardous": True,        
#         "high_demand": False,
#         "discounted": False,
#         "high_theft": False
#     }
# ]

# # Define complementary product pairs (indices)
# complementary_pairs = [(4, 5)]  # (Pasta, Pasta Sauce)