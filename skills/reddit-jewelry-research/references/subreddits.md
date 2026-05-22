# Subreddit Reference

Verify current activity, rules, and member counts before making time-sensitive claims.

## Primary Jewelry Communities

| Subreddit | Priority | Why it matters | Search focus |
|---|---:|---|---|
| r/jewelry | High | Broad jewelry discussions, buying advice, care, materials, rings, necklaces, earrings | tarnish, green skin, everyday jewelry, recommendations, quality |
| r/Earrings | High | Earring comfort, styling, materials, backs, changing habits | sensitive ears, office earrings, flat back, lightweight, everyday earrings |
| r/jewelrymaking | High | Maker-side signals around materials, construction, repair, durability | tarnish, clasp, hinge, broken, repair, titanium, prototype |
| r/jewelers | Medium | Professional jeweler feedback on mechanism, durability, and premium perception | repair, material, setting, clasp, durability |
| r/JewelryDesign | Medium | Design feedback and concept validation; check rules carefully | design feedback, prototype, modular, convertible |
| r/jewellerymaking | Medium | UK/international spelling and maker audience | jewellery, silver, handmade, tarnish |

## Fashion and Workwear Communities

| Subreddit | Priority | Why it matters | Search focus |
|---|---:|---|---|
| r/femalefashionadvice | High | Large fashion advice community with workwear and daily questions | office jewelry, business casual, outfit jewelry |
| r/BusinessFashion | High | Strong match for office-to-evening and professional appropriateness | work appropriate, business casual, office accessories |
| r/fashionwomens35 | High | Mature fashion audience with quality and versatility signals | quality jewelry, polished, capsule, work outfit |
| r/OUTFITS | Medium | Outfit feedback reveals accessory gaps and occasion-fit questions | what jewelry, too much, office outfit, date night |
| r/PetiteFashionAdvice | Medium | Useful for proportion, jewelry scale, small-format accessories | small earrings, delicate jewelry, proportion |
| r/Weddingattireapproval | Medium | Occasion-based styling and formalwear accessory needs | jewelry for dress, earrings, ring, formal |

## Pain-Point Communities

| Subreddit | Priority | Why it matters | Search focus |
|---|---:|---|---|
| r/piercing | High | Strong signal for sensitive ears, material safety, backs, irritation | sensitive ears, titanium, flat back, irritation |
| r/PiercingAdvice | Medium | Practical earring problems and advice requests | irritation, allergic, earring stuck, changing jewelry |
| r/SkincareAddiction | Low | Indirect source for contact dermatitis and skin reaction language | nickel allergy, contact dermatitis, skin reaction |
| r/BuyItForLife | Medium | Durability, quality, long-term value, anti-disposable positioning | quality jewelry, long lasting, tarnish, worth it |

## Capsule, Minimalism, and Travel

| Subreddit | Priority | Why it matters | Search focus |
|---|---:|---|---|
| r/capsulewardrobe | High | Tests jewelry as part of a smaller wardrobe | capsule jewelry, versatile jewelry, accessories |
| r/minimalism | Medium | Tests fewer, better pieces and anti-overconsumption framing | jewelry collection, too much stuff, everyday items |
| r/HerOneBag | High | Travel-light women often care about compact multi-use items | travel jewelry, packing jewelry, one bag accessories |
| r/onebag | Medium | Broader travel-light community; more function-driven | multi-use, travel accessories, packing |

## Validation and Startup Communities

| Subreddit | Priority | Why it matters | Search focus |
|---|---:|---|---|
| r/Entrepreneur | Medium | Reddit-led customer discovery and launch tactics | Reddit marketing, seed users, validation |
| r/smallbusiness | Medium | Small brand operations, positioning, and ecommerce | jewelry business, handmade business, ecommerce |
| r/StreetwearStartup | Low | Community-based product feedback culture, category-adjacent | feedback, drop, brand launch |

## Default Weekly Scrape

Use all 18 communities as the full research universe, but collect them in batches to reduce Reddit blocking risk.

Core batch for the first production pass:

```text
jewelry
Earrings
jewelrymaking
femalefashionadvice
BusinessFashion
fashionwomens35
piercing
HerOneBag
```

Extended batch, only after the core batch succeeds:

```text
capsulewardrobe
BuyItForLife
OUTFITS
PetiteFashionAdvice
Weddingattireapproval
minimalism
onebag
PiercingAdvice
jewelers
JewelryDesign
```

For canary tests, use only `r/jewelry` with one endpoint and a low limit. For production reports, do not permanently drop the extended batch; defer it when the live network path returns 403/429 or when the core batch already exceeds the minimum useful data threshold.
