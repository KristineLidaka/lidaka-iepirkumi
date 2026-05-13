import os
import logging
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
from num2words import num2words

app = Flask(__name__)
CORS(app)

load_dotenv()
level_name = os.environ.get("LOG_LEVEL", "INFO")
logging.basicConfig(level=level_name)


@app.route("/check", methods=["POST"])
def check_article():
    data = request.json
    products = data.get("items", [])
    logging.debug(f"Products: {products}")
    validation_errors = []
    total_cents = 0

    for item in products:
        article = item.get("article")
        mid = len(article) // 2
        quantity = int(item.get("quantity", 0))
        price = float(item.get("price", 0.0))
        logging.debug(f"Article: {article} | Mid: {mid} | Quantity: {quantity} | Price: {price}")

        error_msg = None

        if article.startswith("0"):
            error_msg = "Artikuls nedrīkst sākties ar nulli"
        elif len(article) % 2 == 0 and article[:mid] == article[mid:]:
            error_msg = "Artikuls nedrīkst atkārtoties"
        elif quantity is not None and int(quantity) < 0:
            error_msg = "Daudzums nedrīkst būt negatīvs skaitlis"
        elif price < 0:
            error_msg = "Cena nedrīkst būt negatīva"

        if error_msg:
            logging.debug(f"Validation error for article {article}: {error_msg}")
            validation_errors.append(
                {
                    "uid": item.get("uid"),
                    "article": article,
                    "error_msg": error_msg,
                }
            )
        else:
            price = float(item.get("price", 0.0))
            logging.debug(f"Quantity: {quantity} | Price: {price}")

            total_cents += int(round(quantity * price * 100, 0))

    if validation_errors:
        return jsonify(
            {
                "status": "error",
                "message": f"Validation errors for {len(validation_errors)} items",
                "errors": validation_errors,
            }
        )

    euro, cents = divmod(total_cents, 100)
    logging.debug(f"Total: {total_cents} | Euro: {euro} | Cents: {cents}")

    try:
        euro_text = num2words(euro, lang="lv")
        cents_text = num2words(cents, lang="lv")

        if cents == 1 and cents != 11:
            label_cents = "cents"
        else:
            label_cents = "centi"

        total_sum_text_lv = f"{euro_text} eiro un {cents_text} {label_cents}"
    except (ValueError, TypeError, KeyError) as e:
        logging.error(f"Translation error for euro={euro}, cents={cents}: {e}")
        total_sum_text_lv = "Kļūda tulkojot summu"

    return jsonify(
        {
            "status": "success",
            "total_sum_text_lv": total_sum_text_lv,
        }
    )


@app.route("/health")
def health_check():
    return {"status": "healthy"}, 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
