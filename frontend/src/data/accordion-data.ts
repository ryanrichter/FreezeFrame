export interface AccordionItem {
  id: number;
  product_name: string;
  confidence_score: number;
  description: string;
  potential_retailers: string[];
}

export const accordionData: AccordionItem[] = [
  {
    id: 1,
    "product_name": "Apple iPhone 14",
    "confidence_score": 95,
    "description": "A black smartphone with a dual-camera system, likely an iPhone 14 based on design.",
    "potential_retailers": ["Amazon", "Apple Store", "Best Buy"]
},
{
    id: 2,
    "product_name": "YETI Ceramic Coffee Mug",
    "confidence_score": 80,
    "description": "A solid blue ceramic mug with a handle, standard size.",
    "potential_retailers": ["Amazon", "Walmart", "Target"]
}
]; 