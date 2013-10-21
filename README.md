## OpenContracts.eu

What major purchases have the European governments made recently? Who
are the most prominent contractors? What kinds of services do they 
provide?

This data-driven site will present contract award information from the
combined European procurement system, Tenders Electronic Daily (TED).

#### Features

The site will break down procurement information over a variety of 
dimensions. The key dimensions are: 

* Purpose (based on the Common Procurement Vocabulary, CPV)
* Geography (based on countries, NUTS codes and addresses)
* Supplier (i.e. contract grantee)
* Authority (i.e. public body or quasi-public organisation)

#### Technology 

The application will run on Python, using Flask to render out web 
pages and ``dataset`` for database interaction. Web pages will be
generated statically and then uploaded to S3 to minimize operations 
overhead.

#### Help me out here!

I'm very keen for contributions on this site, please either get started
with pull requests or ping me at friedrich@pudo.org.

