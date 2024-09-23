
# BOOM RENTAL HARMORNY- (BACK-END)
## OVERVIEW
The Boom Rental Management System is designed to streamline property rentals, connecting tenants, landlords, and property managers. This system handles properties, tenants, rent payments, maintenance requests, and more, facilitating efficient management of rental operations. The backend is built to provide RESTful APIs for managing these operations through various entities.

## ERD SUMMARY
The database is organized into several tables that represent the core entities in the system, including:

- Tenants: Manages tenant information.
- Properties: Stores details about properties.
- Agreements: Tracks rental agreements between tenants and landlords.
- Payments: Records rent payments made by tenants.
- Maintenance Requests: Logs maintenance issues reported by tenants.
## KEY ENTITIES:
  1. Tenant

   - Stores information about tenants.
   - Key attributes: tenant_id, name, email, phone_number, house_number, etc.
   - Relations: Linked to agreements (a tenant can have multiple agreements) and payments (a tenant makes multiple payments).

  2. Property

   - Contains details about properties available for rent.
   - Key attributes: property_id, name, location, price, description.
   - Relations: Linked to agreements (a property can have multiple rental agreements).

  3. Agreement

   - Represents the rental agreement between a tenant and the property they are renting.
   - Key attributes: agreement_id, start_date, end_date, rent_amount.
   - Relations: Linked to tenants (each agreement has one tenant) and properties (each agreement involves one property).

  4. Payment

   - Records rent payments made by tenants.
   - Key attributes: payment_id, date, amount, status.
   - Relations: Linked to agreements (each payment is related to one rental agreement).

  5. Maintenance Request

   - Logs maintenance issues that tenants submit for their rented properties.
   - Key attributes: request_id, issue_type, description, status, priority.
   - Relations: Linked to tenants (each request is submitted by a tenant).

## RELATIONS BETWEEN ENTITIES:
  1. Tenant - Agreement - Property: Tenants sign rental agreements to rent properties. A tenant can have multiple agreements over time, and each property can be rented out under different agreements.
  2. Agreement - Payment: Each agreement requires regular payments. Payments are logged to track the fulfillment of rental obligations.
  3. Tenant - Maintenance Request: Tenants can submit maintenance requests related to their rented properties.

## BACKEND STACK
 - Database: PostgreSQL is used for storing and managing relational data. Tables for each entity are designed with necessary foreign keys to maintain relationships.
 - Backend Framework: Node.js with Express.js is used for creating the RESTful APIs.
 - ORM: Sequelize ORM is used to interact with the PostgreSQL database.
 - Authentication: JWT-based authentication system is implemented to secure API routes for tenants, landlords, and staff.
## API ENDPOINTS
1. Tenant Endpoints:
- GET /tenants: Get all tenants.
- GET /tenants/:id: Get details of a specific tenant.
- POST /tenants: Add a new tenant.
- PUT /tenants/:id: Update tenant information.
- DELETE /tenants/:id: Remove a tenant.
2. Property Endpoints:
- GET /properties: List all available properties.
- GET /properties/:id: Get details of a specific property.
- POST /properties: Add a new property.
- PUT /properties/:id: Update property information.
- DELETE /properties/:id: Delete a property.
3. Agreement Endpoints:
- GET /agreements: View all rental agreements.
- GET /agreements/:id: View a specific agreement.
- POST /agreements: Create a new rental agreement.
- PUT /agreements/:id: Update agreement details.
- DELETE /agreements/:id: Cancel an agreement.
4. Payment Endpoints:
- GET /payments: View all payments.
- GET /payments/:id: View a specific payment.
- POST /payments: Record a new payment.
- PUT /payments/:id: Update payment status.
- DELETE /payments/:id: Delete a payment record.
5. Maintenance Request Endpoints:
- GET /maintenance-requests: View all maintenance requests.
- GET /maintenance-requests/:id: View a specific maintenance request.
- POST /maintenance-requests: Submit a new request.
- PUT /maintenance-requests/:id: Update request status.
- DELETE /maintenance-requests/:id: Remove a request.
### Installation and Setup
 1. Clone the repository:
     (git clone)

2. Install dependencies:

  cd backend
  npm install

3. Set up environment variables in a .env file:

 -DB_HOST=localhost
 -DB_USER=your-username
 -DB_PASS=your-password
 -DB_NAME=rental_management
 -JWT_SECRET=your_jwt_secret

4. Run migrations to create tables:

-npx sequelize-cli db:migrate

5. Start the server:

-npm start


 ### Future Features
  - Implement notifications for tenants and staff regarding new maintenance requests and upcoming payment deadlines.
  - Add a reporting dashboard for landlords to view their properties' performance.
  - Include a search feature to filter properties based on location, price, and availability.


# License
This project is licensed under the MIT License.
See the LICENSE file for details