const fetch = require('node-fetch');

async function testAPI() {
  const baseUrl = 'http://localhost:8000';

  // 1. Créer un item
  const newItem = {
    name: "iPhone 13",
    description: "Smartphone Apple",
    price: 999.99
  };

  console.log('1. Création d\'un nouvel item...');
  const createResponse = await fetch(`${baseUrl}/items`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(newItem)
  });
  const createdItem = await createResponse.json();
  console.log('Item créé:', createdItem);

  // 2. Obtenir la liste des items
  console.log('\n2. Obtention de la liste des items...');
  const listResponse = await fetch(`${baseUrl}/items`);
  const items = await listResponse.json();
  console.log('Liste des items:', items);

  // 3. Obtenir un item spécifique
  console.log(`\n3. Obtention de l'item ${createdItem.id}...`);
  const getResponse = await fetch(`${baseUrl}/items/${createdItem.id}`);
  const item = await getResponse.json();
  console.log('Item récupéré:', item);

  // 4. Mettre à jour un item
  const updateData = {
    name: "iPhone 13 Pro",
    description: "Smartphone Apple Premium",
    price: 1299.99
  };

  console.log(`\n4. Mise à jour de l'item ${createdItem.id}...`);
  const updateResponse = await fetch(`${baseUrl}/items/${createdItem.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updateData)
  });
  const updatedItem = await updateResponse.json();
  console.log('Item mis à jour:', updatedItem);

  // 5. Supprimer un item
  console.log(`\n5. Suppression de l'item ${createdItem.id}...`);
  const deleteResponse = await fetch(`${baseUrl}/items/${createdItem.id}`, {
    method: 'DELETE'
  });
  const deleteResult = await deleteResponse.json();
  console.log('Résultat de la suppression:', deleteResult);
}

testAPI().catch(console.error);