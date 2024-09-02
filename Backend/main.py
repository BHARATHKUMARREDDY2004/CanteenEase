from flask import Flask, jsonify, request
import re

app = Flask(__name__)

meals_data = {
    "meals": [
        {
            "idMeal": "1",
            "strMeal": "Chicken Biryani",
            "strCategory": "Starter",
            "strArea": "Block 5",
            "strCanteen": "Spice Corner",
            "strMealThumb": "https://t4.ftcdn.net/jpg/08/24/91/71/240_F_824917190_rfmzNyXz1kES6obVji2PxOXx5CLzQyfM.jpg",
            "strPrice": "₹10.99",
            "strDescription": "Delicious chicken biryani with aromatic spices and tender chicken pieces."
        },
        {
            "idMeal": "2",
            "strMeal": "Vegetable Sandwich",
            "strCategory": "Vegetarian",
            "strArea": "Block 12",
            "strCanteen": "Green Delights",
            "strMealThumb": "https://t3.ftcdn.net/jpg/02/12/66/32/240_F_212663294_PPIXEQMJVZSiKlwMsPBMruuf4Fcctkn9.jpg",
            "strPrice": "₹5.99",
            "strDescription": "A healthy and filling sandwich packed with fresh vegetables and flavorful condiments."
        },
        {
            "idMeal": "3",
            "strMeal": "Paneer Butter Masala",
            "strCategory": "Vegetarian",
            "strArea": "Block 8",
            "strCanteen": "Taste of India",
            "strMealThumb": "https://t3.ftcdn.net/jpg/07/33/35/20/240_F_733352022_Xw1fn7F75GwU9d49iM2fzzayemx5BN1Z.jpg",
            "strPrice": "₹8.99",
            "strDescription": "Creamy and rich paneer butter masala cooked with aromatic spices and served with naan."
        },
        {
            "idMeal": "4",
            "strMeal": "Margherita Pizza",
            "strCategory": "Pasta",
            "strArea": "Block 22",
            "strCanteen": "Italiano Express",
            "strMealThumb": "https://t3.ftcdn.net/jpg/08/21/43/70/240_F_821437091_fZVVfyqTd91FHEdZYhqZ64Jx7UHt6pXm.jpg",
            "strPrice": "₹12.99",
            "strDescription": "Classic margherita pizza with a thin crust, fresh tomatoes, mozzarella cheese, and basil leaves."
        },
        {
            "idMeal": "5",
            "strMeal": "Fried Rice",
            "strCategory": "Breakfast",
            "strArea": "Block 15",
            "strCanteen": "Asian Fusion",
            "strMealThumb": "https://t3.ftcdn.net/jpg/07/23/32/42/240_F_723324248_3IzXtewCSiPHxo2ox5Zz69MBkE51Pjps.jpg",
            "strPrice": "₹7.99",
            "strDescription": "A flavorful and aromatic fried rice dish with a mix of vegetables and soy sauce."
        },
        {
            "idMeal": "6",
            "strMeal": "Chocolate Brownie",
            "strCategory": "Dessert",
            "strArea": "Block 3",
            "strCanteen": "Sweet Treats",
            "strMealThumb": "https://t4.ftcdn.net/jpg/07/57/42/23/240_F_757422313_YmUNJw5N2a1onZkbMEdl9P6WO1DXbJhO.jpg",
            "strPrice": "₹3.99",
            "strDescription": "Decadent and fudgy chocolate brownie topped with a scoop of vanilla ice cream."
        },
        {
            "idMeal": "7",
            "strMeal": "Chicken Tikka Masala",
            "strCategory": "Starter",
            "strArea": "Block 10",
            "strCanteen": "Spice Corner",
            "strMealThumb": "https://t4.ftcdn.net/jpg/05/85/17/03/240_F_585170352_7D9PjNXOvU3PAB4ynMRWpEavhBNuLG3J.jpg",
            "strPrice": "₹11.99",
            "strDescription": "Tender chicken tikka cooked in a creamy and flavorful tomato-based sauce."
        },
        {
            "idMeal": "8",
            "strMeal": "Cheeseburger",
            "strCategory": "Starter",
            "strArea": "Block 18",
            "strCanteen": "Burger Joint",
            "strMealThumb": "https://t4.ftcdn.net/jpg/01/58/69/83/240_F_158698372_6TEPVMocLay9H2xGa3qyYAfHGsxi8Ft5.jpg",
            "strPrice": "₹9.99",
            "strDescription": "Juicy beef patty topped with melted cheese, fresh lettuce, tomatoes, and pickles."
        },
        {
            "idMeal": "9",
            "strMeal": "Pasta Alfredo",
            "strCategory": "Pasta",
            "strArea": "Block 6",
            "strCanteen": "Italiano Express",
            "strMealThumb": "https://t3.ftcdn.net/jpg/07/94/77/76/240_F_794777638_3xgRIqbCLh7vFyttA5A0YrOkFaEk8stD.jpg",
            "strPrice": "₹10.99",
            "strDescription": "Creamy and cheesy pasta alfredo made with fresh parmesan and buttery sauce."
        },
        {
            "idMeal": "10",
            "strMeal": "Fish and Chips",
            "strCategory": "Seafood",
            "strArea": "Block 4",
            "strCanteen": "Seafood Delights",
            "strMealThumb": "https://t3.ftcdn.net/jpg/06/03/98/36/240_F_603983685_yQdt6Cw38M4QChBOvhUiGCC49JMnt12j.jpg",
            "strPrice": "₹13.99",
            "strDescription": "Crispy battered fish served with golden fries and tartar sauce."
        },
        {
            "idMeal": "11",
            "strMeal": "Spaghetti Carbonara",
            "strCategory": "Pasta",
            "strArea": "Block 7",
            "strCanteen": "Pasta Paradise",
            "strMealThumb": "https://t3.ftcdn.net/jpg/07/12/99/21/240_F_712992185_QvgipX3pDtVxQySDxCJ2PbOZV46Btivv.jpg",
            "strPrice": "₹11.49",
            "strDescription": "Classic spaghetti carbonara with creamy egg sauce, crispy bacon, and parmesan cheese."
        },
        {
            "idMeal": "12",
            "strMeal": "Penne Arrabbiata",
            "strCategory": "Pasta",
            "strArea": "Block 9",
            "strCanteen": "The Italian Table",
            "strMealThumb": "https://t3.ftcdn.net/jpg/06/83/88/74/240_F_683887413_0E8uS4rXlK8J2ipwMkEps4XKbs5BGdBi.jpg",
            "strPrice": "₹10.99",
            "strDescription": "Spicy penne pasta tossed in a flavorful tomato sauce with garlic and chili flakes."
        },
        {
            "idMeal": "13",
            "strMeal": "Fettuccine Alfredo",
            "strCategory": "Pasta",
            "strArea": "Block 14",
            "strCanteen": "Pasta House",
            "strMealThumb": "https://t3.ftcdn.net/jpg/07/93/47/99/240_F_793479911_L7VV2ivAFZwZZ8oHJXvdOSHyfwVeKDdT.jpg",
            "strPrice": "₹12.49",
            "strDescription": "Rich and creamy fettuccine alfredo made with parmesan cheese and buttery sauce."
        },
        {
            "idMeal": "14",
            "strMeal": "Lasagna Bolognese",
            "strCategory": "Pasta",
            "strArea": "Block 19",
            "strCanteen": "Italiano Express",
            "strMealThumb": "https://t3.ftcdn.net/jpg/06/72/39/81/240_F_672398131_tgkhh3BqbcFHkZr9sfzAGKae9AmCCOYH.jpg",
            "strPrice": "₹13.99",
            "strDescription": "Layers of pasta, meaty bolognese sauce, and melted cheese baked to perfection."
        },
        {
            "idMeal": "15",
            "strMeal": "Pesto Pasta",
            "strCategory": "Pasta",
            "strArea": "Block 16",
            "strCanteen": "Green Cuisine",
            "strMealThumb": "https://t3.ftcdn.net/jpg/06/79/34/78/240_F_679347861_vy1i5A1OHJ2z3OePdLlEnIZkJh9D5LnW.jpg",
            "strPrice": "₹9.99",
            "strDescription": "Fresh and vibrant pesto pasta made with basil, pine nuts, parmesan cheese, and olive oil."
        },
        {
            "idMeal": "16",
            "strMeal": "Pancakes with Maple Syrup",
            "strCategory": "Breakfast",
            "strArea": "Block 2",
            "strCanteen": "Morning Delights",
            "strMealThumb": "https://t3.ftcdn.net/jpg/03/45/34/22/240_F_345342267_xx1uDeWslYzY0q4b7Jnx1Hcckz6lfb9y.jpg",
            "strPrice": "₹6.99",
            "strDescription": "Fluffy pancakes served with a generous drizzle of maple syrup and a pat of butter."
        },
        {
            "idMeal": "17",
            "strMeal": "Avocado Toast",
            "strCategory": "Breakfast",
            "strArea": "Block 3",
            "strCanteen": "Healthy Start",
            "strMealThumb": "https://t3.ftcdn.net/jpg/01/73/56/39/240_F_173563946_HaTWxGVby7ZSEgHSxO6gV6gVpPBcNNbx.jpg",
            "strPrice": "₹5.49",
            "strDescription": "Sliced avocado on toasted bread with a sprinkle of salt, pepper, and a squeeze of lemon."
        },
        {
            "idMeal": "18",
            "strMeal": "Breakfast Burrito",
            "strCategory": "Breakfast",
            "strArea": "Block 5",
            "strCanteen": "Quick Bites",
            "strMealThumb": "https://t4.ftcdn.net/jpg/02/07/87/25/240_F_207872566_kRQc4HHR4WAVXYGZY3jj8TcOxyom54QQ.jpg",
            "strPrice": "₹7.99",
            "strDescription": "A hearty and filling breakfast burrito stuffed with eggs, cheese, bacon, and vegetables."
        },
        {
            "idMeal": "19",
            "strMeal": "Omelette with Cheese",
            "strCategory": "Breakfast",
            "strArea": "Block 1",
            "strCanteen": "Eggs & More",
            "strMealThumb": "https://t4.ftcdn.net/jpg/02/08/96/57/240_F_208965734_RgvPjpNOOKMFz63f1HXrmFExGggdZMxA.jpg",
            "strPrice": "₹5.99",
            "strDescription": "Fluffy omelette made with eggs and filled with melted cheese and your choice of toppings."
        },
        {
            "idMeal": "20",
            "strMeal": "French Toast",
            "strCategory": "Breakfast",
            "strArea": "Block 4",
            "strCanteen": "Sweet Mornings",
            "strMealThumb": "https://t4.ftcdn.net/jpg/02/75/84/89/240_F_275848917_lSODgNNM1gkKCUi9hVoeveH2xkq9L7jG.jpg",
            "strPrice": "₹6.49",
            "strDescription": "Thick slices of bread soaked in a mixture of eggs, milk, and cinnamon, then fried until golden."
        },
        {
            "idMeal": "21",
            "strMeal": "Grilled Salmon",
            "strCategory": "Seafood",
            "strArea": "Block 3",
            "strCanteen": "Ocean's Delight",
            "strMealThumb": "https://t3.ftcdn.net/jpg/02/47/87/36/240_F_247873691_pch7RZ2bfpQzyPpAA1BHZEmcPZofDb14.jpg",
            "strPrice": "₹14.99",
            "strDescription": "Fresh salmon fillet marinated in herbs and grilled to perfection, served with lemon wedges."
        },
        {
            "idMeal": "22",
            "strMeal": "Shrimp Scampi",
            "strCategory": "Seafood",
            "strArea": "Block 6",
            "strCanteen": "The Seafood Shack",
            "strMealThumb": "https://t3.ftcdn.net/jpg/02/95/98/60/240_F_295986078_kDeRNlI0Mxg59LzpFk9Goh29p5OElXgE.jpg",
            "strPrice": "₹12.49",
            "strDescription": "Tender shrimp sautéed in garlic butter and white wine, served over a bed of pasta."
        },
        {
            "idMeal": "23",
            "strMeal": "Lobster Roll",
            "strCategory": "Seafood",
            "strArea": "Block 8",
            "strCanteen": "Coastal Bites",
            "strMealThumb": "https://t3.ftcdn.net/jpg/02/15/89/94/240_F_215899457_xDH5M2IxF5eYEUo5LpmMr9eTyFDyQs1J.jpg",
            "strPrice": "₹16.99",
            "strDescription": "Buttery lobster meat tossed in a creamy dressing and served in a toasted roll."
        },
        {
            "idMeal": "24",
            "strMeal": "Fish Tacos",
            "strCategory": "Seafood",
            "strArea": "Block 12",
            "strCanteen": "Taco Beach",
            "strMealThumb": "https://t3.ftcdn.net/jpg/02/76/77/04/240_F_276770404_kZosLg3TK98nWY7LdjQH5n8WiGUfZdzk.jpg",
            "strPrice": "₹9.99",
            "strDescription": "Crispy fish fillets wrapped in warm tortillas and topped with fresh salsa and creamy sauce."
        },
        {
            "idMeal": "25",
            "strMeal": "Crispy Calamari",
            "strCategory": "Seafood",
            "strArea": "Block 15",
            "strCanteen": "Fried Favorites",
            "strMealThumb": "https://t3.ftcdn.net/jpg/03/25/98/71/240_F_325987131_ZwFRkq1gLcs60UzWkblAeJflfN83mdFP.jpg",
            "strPrice": "₹10.99",
            "strDescription": "Tender calamari rings coated in a crispy batter and served with a tangy dipping sauce."
        },
        {
            "idMeal": "26",
            "strMeal": "Tiramisu",
            "strCategory": "Dessert",
            "strArea": "Block 2",
            "strCanteen": "Sweet Moments",
            "strMealThumb": "https://t4.ftcdn.net/jpg/03/33/49/55/240_F_333495519_6wQm8s9X4qSPaH1NgcYJ1T1m1cZKBwmj.jpg",
            "strPrice": "₹7.99",
            "strDescription": "Classic Italian dessert made with layers of coffee-soaked ladyfingers and creamy mascarpone."
        },
        {
            "idMeal": "27",
            "strMeal": "Apple Pie",
            "strCategory": "Dessert",
            "strArea": "Block 4",
            "strCanteen": "Home Bakes",
            "strMealThumb": "https://t4.ftcdn.net/jpg/03/11/57/33/240_F_311573383_kRvJ06CegTgJghyoknIWJbOgHMO5NZ4h.jpg",
            "strPrice": "₹5.99",
            "strDescription": "Classic apple pie with a flaky crust, sweet apple filling, and a hint of cinnamon."
        },
    {
        "idMeal": "28",
        "strMeal": "Chocolate Mousse",
        "strCategory": "Dessert",
        "strArea": "Block 7",
        "strCanteen": "Chocolate Heaven",
        "strMealThumb": "https://t3.ftcdn.net/jpg/01/80/54/90/240_F_180549070_4hEZJr5bNwItBVFbXbC1mIVrMB4klQAY.jpg",
        "strPrice": "₹6.49",
        "strDescription": "A rich and creamy Chocolate Mousse, perfect for dessert lovers at Chocolate Heaven in Block 7."
    },
    {
        "idMeal": "32",
        "strMeal": "Spinach and Ricotta Lasagna",
        "strCategory": "Vegetarian",
        "strArea": "Block 10",
        "strCanteen": "Italiano Express",
        "strMealThumb": "https://t3.ftcdn.net/jpg/02/88/13/55/240_F_288135509_JxLl6bDT7u2Vcnk3cEUgF5Zy8bQQoY2W.jpg",
        "strPrice": "₹10.99",
        "strDescription": "Delicious Spinach and Ricotta Lasagna, a vegetarian delight from Italiano Express in Block 10."
    },
    {
        "idMeal": "33",
        "strMeal": "Mushroom Risotto",
        "strCategory": "Vegetarian",
        "strArea": "Block 3",
        "strCanteen": "Rice & Spice",
        "strMealThumb": "https://t3.ftcdn.net/jpg/02/70/57/97/240_F_270579704_BFwHb6cyC2AQzwLBz9itTjkwMjJvQ95L.jpg",
        "strPrice": "₹9.49",
        "strDescription": "Creamy Mushroom Risotto, a vegetarian specialty from Rice & Spice in Block 3."
    },
    {
        "idMeal": "34",
        "strMeal": "Stuffed Bell Peppers",
        "strCategory": "Vegetarian",
        "strArea": "Block 14",
        "strCanteen": "Green Cuisine",
        "strMealThumb": "https://t4.ftcdn.net/jpg/02/57/55/63/240_F_257556344_frrMs7DxsRbJ8W91U9AbzGbLyMDnABhx.jpg",
        "strPrice": "₹7.99",
        "strDescription": "Tasty Stuffed Bell Peppers, a vegetarian treat from Green Cuisine in Block 14."
    },
    {
        "idMeal": "35",
        "strMeal": "Grilled Vegetable Skewers",
        "strCategory": "Vegetarian",
        "strArea": "Block 9",
        "strCanteen": "Healthy Grills",
        "strMealThumb": "https://t4.ftcdn.net/jpg/02/56/37/12/240_F_256371267_Ux0Ipo7kp9g0oLD9m68fjvT4ZIoZXZht.jpg",
        "strPrice": "₹6.99",
        "strDescription": "Healthy Grilled Vegetable Skewers, a vegetarian option from Healthy Grills in Block 9."
    },
    {
        "idMeal": "36",
        "strMeal": "Bruschetta",
        "strCategory": "Starter",
        "strArea": "Block 8",
        "strCanteen": "Italiano Express",
        "strMealThumb": "https://t4.ftcdn.net/jpg/03/25/91/77/240_F_325917716_t5T2t12WKK41Le2cFOn6yf6ctihwqQkS.jpg",
        "strPrice": "₹5.99",
        "strDescription": "Classic Bruschetta, a perfect starter from Italiano Express in Block 8."
    },
    {
        "idMeal": "37",
        "strMeal": "Spring Rolls",
        "strCategory": "Starter",
        "strArea": "Block 6",
        "strCanteen": "Asian Fusion",
        "strMealThumb": "https://t3.ftcdn.net/jpg/02/17/39/94/240_F_217399419_2B3VmIlbREdxYxg5lGd38bInWn1LVgyf.jpg",
        "strPrice": "₹6.49",
        "strDescription": "Crispy Spring Rolls, a delightful starter from Asian Fusion in Block 6."
    },
    {
        "idMeal": "38",
        "strMeal": "Tomato Basil Soup",
        "strCategory": "Starter",
        "strArea": "Block 11",
        "strCanteen": "Soup & Salad",
        "strMealThumb": "https://t3.ftcdn.net/jpg/07/52/45/92/240_F_752459295_zANBQa5CDn7WsR653nAWuPRVdvcc3FrR.jpg",
        "strPrice": "₹4.99",
        "strDescription": "Warm Tomato Basil Soup, a comforting starter from Soup & Salad in Block 11."
    }
    ]
}


@app.route('/meals/category/<category>', methods=['GET'])
def get_meals_by_category(category):
    meals = [meal for meal in meals_data['meals'] if meal['strCategory'].lower() == category.lower()]
    if meals:
        return jsonify({"meals": meals})
    else:
        return jsonify({"meals": []})

@app.route('/meal/<string:meal_id>', methods=['GET'])
def get_meal_detail(meal_id):
    meal = next((meal for meal in meals_data['meals'] if meal['idMeal'] == meal_id), None)
    if meal:
        return jsonify(meal)
    else:
        return jsonify({"error": "Meal not found"}), 404

@app.route('/search', methods=['GET'])
def search_meals():
    query = request.args.get('query', '').lower()

    if query:
        # Use regular expressions for case-insensitive and partial matching
        pattern = re.compile(re.escape(query), re.IGNORECASE)
        results = [
            meal for meal in meals_data['meals']
            if (pattern.search(meal['strMeal']) or
                pattern.search(meal['strCategory']) or
                pattern.search(meal['strArea']) or
                pattern.search(meal['strCanteen']))
        ]
        if results:
            return jsonify({"meals": results})
        else:
            return jsonify({"meals": None})
    else:
        return jsonify({"meals": None})


@app.route('/meals', methods=['GET'])
def get_meals():
    return jsonify(meals_data)

if __name__ == '__main__':
    app.run(debug=True)
