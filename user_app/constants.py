"""Constants shared by templates and the blog category menus."""

# (slug, title) pairs in menu order. Slugs equal ``pytils.slugify(title)``,
# because ``CategoryBlog.save()`` regenerates the slug from the title.
DEFENDERS_CATEGORIES: tuple[tuple[str, str], ...] = (
    ('obslugovuvannya-bez-chergi', 'Обслуговування без черги'),
    ('kabnet-veterana', 'Кабінет ветерана'),
    ('medichn-poslugi-ta-reabltatsya', 'Медичні послуги та реабілітація'),
    ('ekopfo', 'ЕКОПФО'),
    ('sotsaln-programi-ta-plgi', 'Соціальні програми та пільги'),
    ('pdtrimka-rodin-vjskovih', 'Підтримка родин військових'),
    ('korisn-resursi-ta-garyach-ln', 'Корисні ресурси та гарячі лінії'),
)

DEFENDER_SLUGS: tuple[str, ...] = tuple(
    slug for slug, _ in DEFENDERS_CATEGORIES)
