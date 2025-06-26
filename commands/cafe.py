# commands/cafe.py
import discord
from discord.ext import commands
import random
from utils.data_loader import load_cafes
from datetime import datetime
from math import radians, cos, sin, asin, sqrt
from utils.saved_data import save_cafe_for_user, get_saved_cafes

def haversine(lat1, lon1, lat2, lon2):
    # convert degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    km = 6371 * c  # Radius of Earth in kilometers
    return km


cafes = load_cafes()

class CafeCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="cafe")
    async def cafe(self, ctx, city: str):
        city_cafes = [c for c in cafes if c["city"].lower() == city.lower()]
        if not city_cafes:
            await ctx.send(f"😕 No cafes found in {city}. Try another.")
            return

        cafe = random.choice(city_cafes)
        msg = (
            f"☕ **{cafe['name']}** — ⭐ {cafe['stars']}\n"
            f"📍 {cafe['address']}\n"
            f"🌐 [Open in Maps]<https://www.google.com/maps?q={cafe['latitude']},{cafe['longitude']}>")   
        await ctx.send(msg)

    @commands.command(name="topcafes")
    async def topcafes(self, ctx, *, city: str):
        input_city = city.strip().lower()
        city_cafes = [c for c in cafes if c["city"].strip().lower() == input_city]

        if not city_cafes:
            await ctx.send(f"😕 No cafes found in {city}. Try another.")
            return

        top = sorted(city_cafes, key=lambda x: x["stars"], reverse=True)[:5]

        msg = f"🏆 Top cafes in **{city.title()}**:\n"
        for i, c in enumerate(top, 1):
            msg += (
                f"{i}. **{c['name']}** — ⭐ {c['stars']}\n"
                f"   📍 {c['address']}\n"
                f"   🌐 [Map]<https://www.google.com/maps?q={c['latitude']},{c['longitude']}>\n"
            )

        await ctx.send(msg)


    @commands.command(name="recommend")
    async def recommend(self, ctx, city: str, mood: str):
        city = city.lower().strip()
        mood = mood.lower().strip()

        mood_cafes = [
            c for c in cafes
            if c["city"].lower() == city
            and "ambience" in c
            and c["ambience"].get(mood) == True
        ]

        if not mood_cafes:
            await ctx.send(f"😕 No **{mood}** cafes found in {city.title()}.")
            return

        cafe = random.choice(mood_cafes)
        msg = (
            f"🎯 Here's a **{mood}** cafe in **{city.title()}**:\n"
            f"**{cafe['name']}** — ⭐ {cafe['stars']}\n"
            f"📍 {cafe['address']}\n"
            f"🌐 [Open in Maps]<https://www.google.com/maps?q={cafe['latitude']},{cafe['longitude']}>"
        )

        await ctx.send(msg)


    @commands.command(name="cafebyprice")
    async def cafebyprice(self, ctx, city: str, price: int):
        if price not in [1, 2, 3, 4]:
            await ctx.send("⚠️ Please enter a valid price level (1 to 4).")
            return

        city_cafes = [c for c in cafes if c["city"].strip().lower() == city.lower() and c.get("price") == price]

        if not city_cafes:
            await ctx.send(f"😕 No cafes in **{city.title()}** with price level {price}.")
            return

        msg = f"💸 **Cafes in {city.title()} with price level {price}** :\n\n"
        for i, c in enumerate(city_cafes[:5], 1):
            msg += f"{i}. **{c['name']}** — ⭐ {c['stars']} — 📍 {c['address']}\n"
            msg += f"🌐 [Open in Maps]<https://www.google.com/maps?q={c['latitude']},{c['longitude']}>\n\n"


        await ctx.send(msg)


    @commands.command(name="opennow")
    async def opennow(self, ctx, *, city: str):
        now = datetime.now()
        current_day = now.strftime("%A")  # e.g., "Monday"
        current_minutes = now.hour * 60 + now.minute

        city_key = city.lower().strip()

        open_cafes = []
        for cafe in cafes:
            if cafe["city"].lower().strip() != city_key:
                continue

            hours = cafe.get("hours", {})
            today_hours = hours.get(current_day)

            if not today_hours:
                continue

            try:
                open_str, close_str = today_hours.split("-")
                open_hour, open_minute = map(int, open_str.split(":"))
                close_hour, close_minute = map(int, close_str.split(":"))

                open_minutes = open_hour * 60 + open_minute
                close_minutes = close_hour * 60 + close_minute

                # Handle cafes that close after midnight
                if open_minutes <= close_minutes:
                    is_open = open_minutes <= current_minutes <= close_minutes
                else:
                    is_open = current_minutes >= open_minutes or current_minutes <= close_minutes

                if is_open:
                    open_cafes.append(cafe)

            except:
                continue

        if not open_cafes:
            await ctx.send(f"😕 No cafes currently open in **{city.title()}**.")
            return

        msg = f"🕒 **Cafes currently open in {city.title()}**:\n\n"
        for i, c in enumerate(open_cafes[:5], 1):
            msg += (
                f"{i}. **{c['name']}** — ⭐ {c['stars']}\n"
                f"   📍 {c['address']}\n"
                f"   🌐 <https://www.google.com/maps?q={c['latitude']},{c['longitude']}>\n\n"
            )

        await ctx.send(msg)
    
    @commands.command(name="search")
    async def search(self, ctx, *, name: str):
        name=name.lower().strip()

        matches=[ 
            c for c in cafes
            if name in c["name"].lower()]
        
        if not matches:
            await ctx.send(f"😕 No cafes found matching **{name}**.")
            return
        
        cafe=matches[0]

        msg = f"🔎 **Search Result:**\n"
        msg += f"**{cafe['name']}** — ⭐ {cafe['stars']}\n"
        msg += f"📍 {cafe['address']} ({cafe['city']})\n"

        if cafe.get("price"):
            msg += f"💸 Price Level: {cafe['price']}\n"

        if cafe.get("ambience"):
            amb = [k for k, v in cafe["ambience"].items() if v]
            if amb:
                msg += f"🪄 Ambience: {', '.join(amb)}\n"

        msg += f"🌐 <https://www.google.com/maps?q={cafe['latitude']},{cafe['longitude']}>"

        
        await ctx.send(msg)

    @commands.command(name="nearby")
    async def nearby(self, ctx, lat: float, lon: float):
        if not cafes:
            await ctx.send("⚠️ Cafe data not loaded.")
            return

        # Calculate distance for each cafe
        cafes_with_distance = []
        for cafe in cafes:
            try:
                distance = haversine(lat, lon, cafe["latitude"], cafe["longitude"])
                cafes_with_distance.append((cafe, distance))
            except:
                continue  # skip if coordinates are invalid

        if not cafes_with_distance:
            await ctx.send("😕 Couldn't find cafes near that location.")
            return

        # Sort by distance and take top 5
        closest = sorted(cafes_with_distance, key=lambda x: x[1])[:5]

        msg = "📍 **Cafes near you:**\n\n"
        for i, (cafe, dist) in enumerate(closest, 1):
            msg += (
                f"{i}. **{cafe['name']}** — ⭐ {cafe['stars']}, {dist:.2f} km away\n"
                f"   📍 {cafe['address']}\n"
                f"   🌐 <https://www.google.com/maps?q={cafe['latitude']},{cafe['longitude']}>\n\n"
            )

        await ctx.send(msg)

    @commands.command(name="savecafe")
    async def savecafe(self, ctx, *, name: str):
        matches = [c for c in cafes if name.lower() in c["name"].lower()]
        if not matches:
            await ctx.send("❌ Cafe not found.")
            return

        cafe = matches[0]
        save_cafe_for_user(ctx.author.id, cafe)
        await ctx.send(f"✅ Saved **{cafe['name']}** to your favorites!")

    @commands.command(name="mycafes")
    async def mycafes(self, ctx):
        saved = get_saved_cafes(ctx.author.id)
        if not saved:
            await ctx.send("📭 You haven't saved any cafes yet.")
            return

        msg = f"📌 **Your Saved Cafes:**\n\n"
        for i, cafe in enumerate(saved, 1):
            msg += (
                f"{i}. **{cafe['name']}** — ⭐ {cafe['stars']} — {cafe['city']}\n"
                f"📍 {cafe['address']}\n"
                f"🌐 [Map]<https://www.google.com/maps?q={cafe['latitude']},{cafe['longitude']}>\n\n"
            )

        await ctx.send(msg)

    @commands.command(name="help")
    async def help(self, ctx):
        embed = discord.Embed(
            title="📖 Rush Help Menu",
            description="Here's a list of commands you can use:",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="☕ `!cafe <city>`",
            value="Get a random cafe in the specified city.",
            inline=False
        )
        embed.add_field(
            name="🏆 `!topcafes <city>`",
            value="List top-rated cafes in the city.",
            inline=False
        )
        embed.add_field(
            name="🎯 `!recommend <city> <mood>`",
            value="Get a cafe based on your mood (e.g. casual, trendy, romantic).",
            inline=False
        )
        embed.add_field(
            name="💸 `!cafebyprice <city> <1-4>`",
            value="Find cafes by price level (1 = cheap, 4 = expensive).",
            inline=False
        )
        embed.add_field(
            name="🕒 `!opennow <city>`",
            value="Find cafes currently open in your city.",
            inline=False
        )
        embed.add_field(
            name="🔎 `!search <name>`",
            value="Search for a specific cafe by name.",
            inline=False
        )
        embed.add_field(
            name="📍 `!nearby <latitude> <longitude>`",
            value="Find cafes near a specific location.",
            inline=False
        )
        embed.add_field(
            name="📌 `!savecafe <name>`",
            value="Save a cafe to your personal favorites list.",
            inline=False
        )
        embed.add_field(
            name="📂 `!mycafes`",
            value="View your list of saved cafes.",
            inline=False
        )

        embed.set_footer(text="Enjoy your cafe hunt! ☕")

        await ctx.send(embed=embed)



async def setup(bot):
    await bot.add_cog(CafeCommands(bot))