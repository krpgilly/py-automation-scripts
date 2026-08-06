# TODO: write function to convert price + weight into price per 100g
# TODO: handle edge cases (e.g., missing weight)


def normalize_price(price_str, weight_str):
    """
    Convert raw price + weight strings into price per 100g.
    Example:
        price_str = "£1.49"
        weight_str = "200g"
        returns 0.745 (price per 100g)
        """

    price = float(price_str.replace("£", "").strip())

    weight = float(weight_str.replace("g", "").strip())

    price_per_100g = (price / weight) * 100

    return round(price_per_100g, 3)