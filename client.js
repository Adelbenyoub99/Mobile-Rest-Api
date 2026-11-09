/**
 * Mobile REST API - Node.js Automated E2E Demonstration Client
 * Simulates a mobile client making CRUD requests against the FastAPI backend.
 * Run with: npm start
 */

const fetch = require('node-fetch');

const BASE_URL = process.env.API_URL || 'http://localhost:8000';

async function runDemo() {
  console.log('====================================================');
  console.log('🚀 Mobile REST API - Automated Client Demonstration');
  console.log(`🌐 Target Server: ${BASE_URL}`);
  console.log('====================================================\n');

  try {
    // 0. Healthcheck
    console.log('📡 Step 0: Checking API Health & Info...');
    const healthRes = await fetch(`${BASE_URL}/health`);
    if (!healthRes.ok) {
      throw new Error(`Server unreachable at ${BASE_URL}. Ensure 'python main.py' is running!`);
    }
    const health = await healthRes.json();
    console.log('   ✅ Health status:', JSON.stringify(health));

    // 1. Create a product
    console.log('\n➕ Step 1: Creating a new product...');
    const newItem = {
      name: 'Google Pixel 9 Pro',
      description: 'Smartphone haut de gamme avec puce Google Tensor G4 et IA intégrée',
      category: 'Smartphones',
      price: 1099.00,
      in_stock: true
    };
    const createRes = await fetch(`${BASE_URL}/items`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newItem)
    });
    const createdItem = await createRes.json();
    console.log(`   ✅ Created item #${createdItem.id}: "${createdItem.name}" (${createdItem.price} €)`);

    // 2. Fetch list
    console.log('\n📋 Step 2: Fetching product list (filtered by category "Smartphones")...');
    const listRes = await fetch(`${BASE_URL}/items?category=Smartphones&limit=5`);
    const list = await listRes.json();
    console.log(`   ✅ Retrieved ${list.length} smartphones:`);
    list.forEach(p => console.log(`      - [ID: ${p.id}] ${p.name} - ${p.price} €`));

    // 3. Update product
    console.log(`\n✏️ Step 3: Updating product #${createdItem.id} price & availability...`);
    const updateRes = await fetch(`${BASE_URL}/items/${createdItem.id}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ price: 999.00, in_stock: false })
    });
    const updated = await updateRes.json();
    console.log(`   ✅ Updated price: ${updated.price} € (In stock: ${updated.in_stock})`);

    // 4. Delete product
    console.log(`\n🗑️ Step 4: Deleting product #${createdItem.id}...`);
    const deleteRes = await fetch(`${BASE_URL}/items/${createdItem.id}`, { method: 'DELETE' });
    const deleteMsg = await deleteRes.json();
    console.log(`   ✅ ${deleteMsg.message}`);

    console.log('\n====================================================');
    console.log('🎉 All mobile CRUD operations executed successfully!');
    console.log('📖 Interactive Swagger documentation at: http://localhost:8000/docs');
    console.log('====================================================');
  } catch (err) {
    console.error('\n❌ Execution error:', err.message);
  }
}

runDemo();
