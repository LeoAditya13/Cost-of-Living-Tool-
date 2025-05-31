from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_csv("D:\My Programs\Cost Of Living Tool\\archive\cost-of-living_v2.csv")
df.columns = [col.strip().lower() for col in df.columns]
df['city'] = df['city'].str.strip().str.lower()
cities = sorted(df['city'].unique())

# Mapping of all 55 fields
labels = {
    f'x{i}': label for i, label in enumerate([
        "Meal, Inexpensive Restaurant (USD)",
        "Meal for 2 People, Mid-range Restaurant (USD)",
        "McMeal at McDonalds (USD)",
        "Domestic Beer (Restaurant, 0.5L) (USD)",
        "Imported Beer (Restaurant, 0.33L) (USD)",
        "Cappuccino (USD)",
        "Coke/Pepsi (0.33L, Restaurant) (USD)",
        "Water (0.33L, Restaurant) (USD)",
        "Milk (1L) (USD)",
        "Bread (500g) (USD)",
        "Rice (1kg) (USD)",
        "Eggs (12) (USD)",
        "Local Cheese (1kg) (USD)",
        "Chicken Fillets (1kg) (USD)",
        "Beef Round (1kg) (USD)",
        "Apples (1kg) (USD)",
        "Banana (1kg) (USD)",
        "Oranges (1kg) (USD)",
        "Tomato (1kg) (USD)",
        "Potato (1kg) (USD)",
        "Onion (1kg) (USD)",
        "Lettuce (1 head) (USD)",
        "Water (1.5L, Market) (USD)",
        "Bottle of Wine (Mid-Range) (USD)",
        "Domestic Beer (0.5L, Market) (USD)",
        "Imported Beer (0.33L, Market) (USD)",
        "Cigarettes 20 Pack (Marlboro) (USD)",
        "One-way Ticket (Local Transport) (USD)",
        "Monthly Pass (USD)",
        "Taxi Start (USD)",
        "Taxi 1km (USD)",
        "Taxi 1 Hour Waiting (USD)",
        "Gasoline (1L) (USD)",
        "Volkswagen Golf (New Car) (USD)",
        "Toyota Corolla (New Car) (USD)",
        "Basic Utilities (85m2 Apartment) (USD)",
        "Mobile Tariff (1 min) (USD)",
        "Internet (Unlimited, 60 Mbps+) (USD)",
        "Fitness Club (Monthly) (USD)",
        "Tennis Court Rent (1 hour weekend) (USD)",
        "Cinema (1 Seat) (USD)",
        "Preschool (Monthly) (USD)",
        "International School (Yearly) (USD)",
        "1 Pair of Jeans (Levis etc.) (USD)",
        "1 Summer Dress (Chain Store) (USD)",
        "Nike Running Shoes (USD)",
        "Men Leather Shoes (USD)",
        "1BR Apartment in City Centre (USD)",
        "1BR Apartment Outside Centre (USD)",
        "3BR Apartment in City Centre (USD)",
        "3BR Apartment Outside Centre (USD)",
        "Price per m² (City Centre) (USD)",
        "Price per m² (Outside Centre) (USD)",
        "Average Monthly Net Salary (USD)",
        "Mortgage Interest Rate (%)"
    ], 1)
}

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html", cities=cities)

@app.route("/compare", methods=["POST"])
def compare():
    city1 = request.form['city1'].strip().lower()
    city2 = request.form['city2'].strip().lower()

    row1 = df[df['city'] == city1].squeeze()
    row2 = df[df['city'] == city2].squeeze()

    comparison = []
    for key, label in labels.items():
        v1 = row1.get(key, float('nan'))
        v2 = row2.get(key, float('nan'))
        try:
            diff = ((v2 - v1) / v1) * 100 if v1 != 0 else float('inf')
            change = f"{diff:.2f}% {'↑' if diff > 0 else '↓'}"
        except:
            change = "N/A"
        comparison.append({
            "metric": label,
            "value1": f"{v1:.2f}" if pd.notna(v1) else "N/A",
            "value2": f"{v2:.2f}" if pd.notna(v2) else "N/A",
            "diff": change
        })

    return render_template("compare.html", city1=city1.title(), city2=city2.title(), comparison=comparison)

if __name__ == "__main__":
    app.run(debug=True)
