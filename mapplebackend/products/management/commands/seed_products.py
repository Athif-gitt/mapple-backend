from django.core.management.base import BaseCommand
from products.models import Product

class Command(BaseCommand):
    help = "Seed products safely"

    def handle(self, *args, **kwargs):
        products = [
    {
        "name": "iPhone 17 Pro",
        "category": "iPhone",
        "price": 1299,
        "description": "The latest iPhone 17 Pro with A19 Bionic chip and Dynamic Island.",
        "image": "https://cdn.tmobile.com/content/dam/t-mobile/en-p/cell-phones/apple/Apple-iPhone-17-Pro/Cosmic-Orange/Apple-iPhone-17-Pro-Cosmic-Orange-thumbnail_v1.png"
    },
    {
        "name": "iPhone 16e",
        "category": "iPhone",
        "price": 899,
        "description": "iPhone 16e with A17 Bionic chip and Dynamic Island.",
        "image": "https://store.storeimages.cdn-apple.com/1/as-images.apple.com/is/iphone-compare-iphone-16e-202509_FMT_WHH?wid=248&hei=324&fmt=jpeg&qlt=90"
    },
    {
        "name": "iPhone 15",
        "category": "iPhone",
        "price": 799,
        "description": "iPhone 15 with A16 Bionic chip and all-day battery life.",
        "image": "https://m.media-amazon.com/images/I/71d7rfSl0wL._SL1500_.jpg"
    },
    {
        "name": "iPhone 14 Pro",
        "category": "iPhone",
        "price": 699,
        "description": "iPhone 14 Pro with A16 Bionic chip and ProMotion display.",
        "image": "https://m.media-amazon.com/images/I/61XO4bORHUL._UF1000,1000_QL80_.jpg"
    },
    {
        "name": "iPhone 13",
        "category": "iPhone",
        "price": 599,
        "description": "iPhone 13 with A15 Bionic chip and dual-camera system.",
        "image": "https://m.media-amazon.com/images/I/71GLMJ7TQiL._SL1500_.jpg"
    },
    {
        "name": "MacBook Pro 16” (M3 Pro)",
        "category": "MacBook",
        "price": 2499,
        "description": "MacBook Pro 16-inch with M3 Pro chip and Liquid Retina XDR display.",
        "image": "https://media-ik.croma.com/prod/https://media.tatacroma.com/Croma%20Assets/Computers%20Peripherals/Laptop/Images/302728_xuqn9z.png?tr=w-1000"
    },
    {
        "name": "MacBook Pro 14” (M2 Pro)",
        "category": "MacBook",
        "price": 1999,
        "description": "MacBook Pro 14-inch with M2 Pro chip and ProMotion display.",
        "image": "https://m.media-amazon.com/images/I/61L5QgPvgqL._SL1500_.jpg"
    },
    {
        "name": "MacBook Air 13” (M2)",
        "category": "MacBook",
        "price": 1199,
        "description": "MacBook Air with M2 chip, thin and lightweight design.",
        "image": "https://m.media-amazon.com/images/I/71eXNIDUGjL._SX679_.jpg"
    },
    {
        "name": "MacBook Air 13” (M1)",
        "category": "MacBook",
        "price": 899,
        "description": "MacBook Air with M1 chip, fanless design and Retina display.",
        "image": "https://m.media-amazon.com/images/I/71TPda7cwUL._SL1500_.jpg"
    },
    {
        "name": "AirPods Pro (2nd Gen)",
        "category": "AirPods",
        "price": 249,
        "description": "AirPods Pro with Active Noise Cancellation and Adaptive Transparency.",
        "image": "https://m.media-amazon.com/images/I/61SUj2aKoEL._SL1500_.jpg"
    },
    {
        "name": "AirPods (3rd Gen)",
        "category": "AirPods",
        "price": 179,
        "description": "AirPods 3rd Gen with Spatial Audio and longer battery life.",
        "image": "https://m.media-amazon.com/images/I/61CVih3UpdL._SL1500_.jpg"
    },
    {
        "name": "AirPods Max",
        "category": "AirPods",
        "price": 549,
        "description": "AirPods Max with high-fidelity audio and Active Noise Cancellation.",
        "image": "https://m.media-amazon.com/images/I/71QFjliR-ML._AC_UY436_FMwebp_QL65_.jpg"
    }
]

        for data in products:
            Product.objects.get_or_create(
                name=data["name"],
                defaults=data
            )
        self.stdout.write(
            self.style.SUCCESS("✅ Products seeded successfully")
        )
            
