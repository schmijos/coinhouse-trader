# coinhouse-trader

This was a project where I tried to automatically receive bitcoins and sell them immediately.

It generates a pool of new receiving addresses. These addresses are reported to a REST API which saves them as available into a database. Available addresses are then shown to customers as *ready for payment*.

After receiving payments it notifies the REST API about the address which has received bitcoins. The web app then notifies the customer about the receiving.

After the REST API has cleared the payment the bitcoins are automatically sold to some trader like kraken.

This project should have been a proof of concept for a very new idea but it's neither finished nor has it been run in a production environment. We were mainly hit by the successful founding of coinbase.
