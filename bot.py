import os
import csv

from dotenv import load_dotenv

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes
)

from openpyxl import Workbook

from services.openstreetmap import (
    search_business,
    CATEGORY_MAP
)


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")


# ========================================
# START
# ========================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    categories = ", ".join(
        CATEGORY_MAP.keys()
    )

    await update.message.reply_text(
        "🚀 Business Finder Bot\n\n"

        "Find businesses using:\n\n"

        "/find <category> <city> [radius]\n\n"

        "Examples:\n"
        "/find restaurant Bhopal\n"
        "/find cafe Jaipur\n"
        "/find gym Indore 10\n"
        "/find pharmacy Delhi 5\n\n"

        "📏 Default radius: 5 km\n"
        "📏 Maximum radius: 50 km\n\n"

        f"🏢 Available categories:\n"
        f"{categories}"
    )


# ========================================
# CREATE CSV
# ========================================

def create_csv(
    results,
    category,
    city
):

    safe_city = city.replace(
        " ",
        "_"
    )

    filename = (
        f"{category}_{safe_city}.csv"
    )

    with open(
        filename,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "Business Name",
            "Category",
            "Address",
            "Phone",
            "Website",
            "Latitude",
            "Longitude",
            "Distance KM"
        ])

        for place in results:

            writer.writerow([
                place.get(
                    "name",
                    "Not available"
                ),

                category,

                place.get(
                    "display_name",
                    "Not available"
                ),

                place.get(
                    "phone",
                    "Not available"
                ),

                place.get(
                    "website",
                    "Not available"
                ),

                place.get(
                    "lat",
                    ""
                ),

                place.get(
                    "lon",
                    ""
                ),

                place.get(
                    "distance",
                    ""
                )
            ])

    return filename


# ========================================
# CREATE EXCEL
# ========================================

def create_excel(
    results,
    category,
    city
):

    safe_city = city.replace(
        " ",
        "_"
    )

    filename = (
        f"{category}_{safe_city}.xlsx"
    )

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Businesses"


    # Header

    headers = [
        "Business Name",
        "Category",
        "Address",
        "Phone",
        "Website",
        "Latitude",
        "Longitude",
        "Distance KM"
    ]

    sheet.append(headers)


    # Data

    for place in results:

        sheet.append([

            place.get(
                "name",
                "Not available"
            ),

            category,

            place.get(
                "display_name",
                "Not available"
            ),

            place.get(
                "phone",
                "Not available"
            ),

            place.get(
                "website",
                "Not available"
            ),

            place.get(
                "lat",
                ""
            ),

            place.get(
                "lon",
                ""
            ),

            place.get(
                "distance",
                ""
            )
        ])


    # Column widths

    sheet.column_dimensions["A"].width = 30
    sheet.column_dimensions["B"].width = 15
    sheet.column_dimensions["C"].width = 60
    sheet.column_dimensions["D"].width = 20
    sheet.column_dimensions["E"].width = 40
    sheet.column_dimensions["F"].width = 15
    sheet.column_dimensions["G"].width = 15
    sheet.column_dimensions["H"].width = 15


    workbook.save(filename)

    return filename


# ========================================
# FIND BUSINESS
# ========================================

async def find_business(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    # --------------------------------
    # Validate arguments
    # --------------------------------

    if len(context.args) < 2:

        await update.message.reply_text(

            "❌ Invalid format.\n\n"

            "Use:\n\n"

            "/find restaurant Bhopal\n"
            "/find cafe Jaipur\n"
            "/find gym Indore 10\n\n"

            "Last number = radius in km."
        )

        return


    # --------------------------------
    # Category
    # --------------------------------

    category = (
        context.args[0]
        .lower()
    )


    # --------------------------------
    # Validate category
    # --------------------------------

    if category not in CATEGORY_MAP:

        available_categories = ", ".join(
            CATEGORY_MAP.keys()
        )

        await update.message.reply_text(

            f"❌ Unsupported category:\n"
            f"{category}\n\n"

            f"Available categories:\n"
            f"{available_categories}"
        )

        return


    # --------------------------------
    # City + Radius
    # --------------------------------

    radius = 5

    last_argument = context.args[-1]


    try:

        possible_radius = int(
            last_argument
        )

        if len(context.args) >= 3:

            radius = possible_radius

            city = " ".join(
                context.args[1:-1]
            )

        else:

            city = " ".join(
                context.args[1:]
            )

    except ValueError:

        city = " ".join(
            context.args[1:]
        )


    # --------------------------------
    # Validate city
    # --------------------------------

    if not city.strip():

        await update.message.reply_text(
            "❌ Please enter a city."
        )

        return


    # --------------------------------
    # Validate radius
    # --------------------------------

    if radius <= 0:

        await update.message.reply_text(
            "❌ Radius must be greater than 0 km."
        )

        return


    if radius > 50:

        await update.message.reply_text(
            "❌ Maximum radius is 50 km."
        )

        return


    # --------------------------------
    # Searching
    # --------------------------------

    await update.message.reply_text(

        "🔎 Searching...\n\n"

        f"🏢 Category: {category.title()}\n"
        f"📍 City: {city}\n"
        f"📏 Radius: {radius} km"
    )


    # ========================================
    # SEARCH
    # ========================================

    try:

        results = search_business(
            category,
            city,
            radius
        )


        # --------------------------------
        # No results
        # --------------------------------

        if not results:

            await update.message.reply_text(

                "❌ No businesses found.\n\n"

                "Try another city or category."
            )

            return


        # --------------------------------
        # Maximum 10 Telegram results
        # --------------------------------

        results = results[:10]


        # ========================================
        # RESULTS
        # ========================================

        message = (

            f"🏢 *{category.title()}s*\n"
            f"📍 {city}\n"
            f"📏 Radius: {radius} km\n"
            f"📊 Showing: {len(results)} results\n\n"
        )


        for index, place in enumerate(
            results,
            start=1
        ):

            name = place.get(
                "name",
                "Business name unavailable"
            )

            address = place.get(
                "display_name",
                "Address unavailable"
            )

            phone = place.get(
                "phone",
                "Not available"
            )

            website = place.get(
                "website",
                "Not available"
            )

            distance = place.get(
                "distance",
                "Not available"
            )

            lat = place.get("lat")
            lon = place.get("lon")


            # --------------------------------
            # Map URL
            # --------------------------------

            if lat and lon:

                map_url = (
                    "https://www.openstreetmap.org/"
                    f"?mlat={lat}"
                    f"&mlon={lon}"
                    f"#map=18/{lat}/{lon}"
                )

            else:

                map_url = (
                    "https://www.openstreetmap.org/"
                )


            # --------------------------------
            # Business
            # --------------------------------

            message += (

                f"*{index}. {name}*\n"

                f"📍 {address}\n"

                f"📏 {distance} km\n"

                f"📞 {phone}\n"

                f"🌐 {website}\n\n"
            )


            # --------------------------------
            # Buttons
            # --------------------------------

            buttons = [

                [
                    InlineKeyboardButton(
                        "🗺️ Open Map",
                        url=map_url
                    )
                ]

            ]


            # Phone button

            if (
                phone
                and phone != "Not available"
            ):

                phone_clean = (
                    phone
                    .replace(" ", "")
                    .replace("-", "")
                )

                buttons.append([

                    InlineKeyboardButton(
                        "📞 Call",
                        url=f"tel:{phone_clean}"
                    )

                ])


            # Website button

            if (
                website
                and website != "Not available"
            ):

                if not website.startswith(
                    "http"
                ):

                    website = (
                        "https://"
                        + website
                    )

                buttons.append([

                    InlineKeyboardButton(
                        "🌐 Website",
                        url=website
                    )

                ])


            await update.message.reply_text(

                (
                    f"🏢 *{name}*\n\n"

                    f"📍 {address}\n"

                    f"📏 Distance: "
                    f"{distance} km\n"

                    f"📞 {phone}\n"

                    f"🌐 {website}"
                ),

                parse_mode="Markdown",

                reply_markup=InlineKeyboardMarkup(
                    buttons
                ),

                disable_web_page_preview=True
            )


        # ========================================
        # EXPORT FILES
        # ========================================

        csv_file = create_csv(
            results,
            category,
            city
        )

        excel_file = create_excel(
            results,
            category,
            city
        )


        # --------------------------------
        # Send CSV
        # --------------------------------

        with open(
            csv_file,
            "rb"
        ) as file:

            await update.message.reply_document(

                document=file,

                filename=os.path.basename(
                    csv_file
                ),

                caption=(
                    "📊 CSV Export\n\n"
                    f"🏢 {category.title()}\n"
                    f"📍 {city}\n"
                    f"📏 {radius} km"
                )
            )


        # --------------------------------
        # Send Excel
        # --------------------------------

        with open(
            excel_file,
            "rb"
        ) as file:

            await update.message.reply_document(

                document=file,

                filename=os.path.basename(
                    excel_file
                ),

                caption=(
                    "📗 Excel Export\n\n"
                    f"🏢 {category.title()}\n"
                    f"📍 {city}\n"
                    f"📏 {radius} km"
                )
            )


        # --------------------------------
        # Delete temporary files
        # --------------------------------

        os.remove(csv_file)
        os.remove(excel_file)


    # ========================================
    # ERROR
    # ========================================

    except Exception as e:

        print(
            "ERROR:",
            repr(e)
        )

        await update.message.reply_text(

            "⚠️ Search failed.\n\n"

            "The OpenStreetMap service may be "
            "temporarily unavailable.\n\n"

            "Please try again later."
        )


# ========================================
# MAIN
# ========================================

def main():

    if not BOT_TOKEN:

        print(
            "❌ BOT_TOKEN not found in .env"
        )

        return


    app = (

        ApplicationBuilder()

        .token(BOT_TOKEN)

        .build()
    )


    # Commands

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "find",
            find_business
        )
    )


    print(
        "🤖 Business Finder Bot running..."
    )


    app.run_polling()


# ========================================
# ENTRY POINT
# ========================================

if __name__ == "__main__":

    main()