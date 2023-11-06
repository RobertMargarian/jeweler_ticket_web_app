from django.test import TestCase
from customers.models import Company, Owner, Client, Order

class StartTest(TestCase):
    def setUp(self):
        # Create a Company
        self.company = Company.objects.create(
            company_name="Test Company",
            company_address_lines="123 Test Street",
            company_city="Testville",
            company_state="Test State",
            company_zip="91203",
            
            )
        
        # Create an Owner
        self.owner = Owner.objects.create(name="Owner Name", company=self.company)
    
    def test_create_clients_and_orders(self):
        # Create 10 clients
        for i in range(10):
            client = Client.objects.create(name=f"Client {i}", owner=self.owner, company=self.company)
            
            # Create 2 orders for each client
            for j in range(2):
                order = Order.objects.create(client=client, description=f"Order {i}-{j}")
                
                # Create notes for some orders
                if i % 2 == 0:
                    order.notes.create(content=f"Note for Order {i}-{j}")
    
    def test_some_other_test(self):
        # Another test case
        # ...
