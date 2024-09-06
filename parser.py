import re

texts = [
    """
The following error has been reported at
August 25 2024 00:05:52UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
Bellow are relevant details of error:
Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
Workflow Title: BraintreeDisputeToSiftChargeback
Step Name:  terminate-3
""",
    """
    The following error has been reported at
    August 25 2024 01:23:03UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 25 2024 04:03:27UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    Step Name:  checkout-1
    """,
    """
    The following error has been reported at
    August 25 2024 05:33:02UTC from one of your Tray.io integrations: 100.00%  ( 16/ 16) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 87432b18-50e9-466e-b413-1d67ae88b604
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a57e604e-3669-4ff6-ac4e-b0558b216f30
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 25 2024 09:54:01UTC from one of your Tray.io integrations: 83.77%  ( 805/ 961) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fab4769d-31ec-49e5-8a98-200854a71eaa
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 25 2024 10:02:46UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 472fafc5-2f7e-422f-8eee-448c3c257b6e
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: db8ac78b-049a-4e2b-b145-1f7a3610165f
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 25 2024 12:12:02UTC from one of your Tray.io integrations: 100.00%  ( 16/ 16) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 693668a4-5787-4d9a-8677-28da5c481049
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: ebda89e5-64c0-4987-af27-095fa076a2bb
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 25 2024 15:46:45UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: 5cd14ea0-bfdb-477c-9ff4-6667f2887d89
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: f1071e14-038c-4cb7-a158-114a00d77b05
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 25 2024 18:04:33UTC from one of your Tray.io integrations: no matching public key
    Bellow are relevant details of error:
    Solution Instance ID: cb6eae2d-2cec-4044-9901-71b533912e4e
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 4e2c50d1-83f8-4ab4-8d46-9285e7ed1049
    Workflow Title: BraintreeDisputeToSiftChargeback
    Step Name:  trigger
    """,
    """
    The following error has been reported at
    August 25 2024 19:40:01UTC from one of your Tray.io integrations: 3.75%  ( 9/ 240) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 5c458ce5-505b-4425-9138-38ad67099816
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 25 2024 19:56:02UTC from one of your Tray.io integrations: 58.33%  ( 28/ 48) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fd662297-e73b-4148-9f66-dd585b5e1db8
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a446880c-742b-4b01-b2f5-20fcc5359a64
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 25 2024 20:18:01UTC from one of your Tray.io integrations: 100.00%  ( 5/ 5) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 514220e6-6dfd-4f37-8028-fe946b91016e
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 39eb56f2-76de-427a-94dd-f7d9465856fe
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 00:05:43UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    Step Name:  terminate-3
    """,
    """
    The following error has been reported at
    August 26 2024 01:46:42UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 26 2024 02:03:13UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    Step Name:  checkout-1
    """,
    """
    The following error has been reported at
    August 26 2024 03:42:02UTC from one of your Tray.io integrations: 100.00%  ( 1/ 1) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 689b5e27-2e91-4e78-bf0d-f6b3272cdf95
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 5068265c-3437-4502-8dda-0f8f7a5a595d
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 05:33:02UTC from one of your Tray.io integrations: 100.00%  ( 8/ 8) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 87432b18-50e9-466e-b413-1d67ae88b604
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a57e604e-3669-4ff6-ac4e-b0558b216f30
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 06:46:49UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: 5cd14ea0-bfdb-477c-9ff4-6667f2887d89
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: f1071e14-038c-4cb7-a158-114a00d77b05
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 26 2024 07:15:11UTC from one of your Tray.io integrations: no matching public key
    Bellow are relevant details of error:
    Solution Instance ID: cb6eae2d-2cec-4044-9901-71b533912e4e
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 4e2c50d1-83f8-4ab4-8d46-9285e7ed1049
    Workflow Title: BraintreeDisputeToSiftChargeback
    Step Name:  trigger
    """,
    """
    The following error has been reported at
    August 26 2024 09:00:03UTC from one of your Tray.io integrations: 100.00%  ( 2/ 2) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: a8b12d30-fa51-4fb1-a56c-d15197f2d0ff
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 3a8117c7-0607-4c84-b638-1ac652f2586c
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 09:54:01UTC from one of your Tray.io integrations: 80.30%  ( 856/ 1066) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fab4769d-31ec-49e5-8a98-200854a71eaa
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 11:58:12UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 3006c145-bd8a-490d-9ad0-368faf01828d
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 26 2024 12:12:02UTC from one of your Tray.io integrations: 100.00%  ( 9/ 9) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 693668a4-5787-4d9a-8677-28da5c481049
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: ebda89e5-64c0-4987-af27-095fa076a2bb
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 12:55:26UTC from one of your Tray.io integrations: Cannot read properties of undefined (reading 'id')
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 26 2024 14:48:33UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 650dcdf4-b498-4638-acb5-67f5aeaa7349
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 2cfba886-611b-41c5-a442-0be625f7dd78
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 26 2024 14:57:46UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 472fafc5-2f7e-422f-8eee-448c3c257b6e
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: db8ac78b-049a-4e2b-b145-1f7a3610165f
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 26 2024 19:40:02UTC from one of your Tray.io integrations: 4.24%  ( 50/ 1180) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 5c458ce5-505b-4425-9138-38ad67099816
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 19:56:02UTC from one of your Tray.io integrations: 45.59%  ( 93/ 204) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fd662297-e73b-4148-9f66-dd585b5e1db8
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a446880c-742b-4b01-b2f5-20fcc5359a64
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 20:18:01UTC from one of your Tray.io integrations: 100.00%  ( 2/ 2) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 514220e6-6dfd-4f37-8028-fe946b91016e
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 39eb56f2-76de-427a-94dd-f7d9465856fe
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 21:35:09UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.data.attributes in property: 'object' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  object-helpers-1
    """,
    """
    The following error has been reported at
    August 27 2024 00:06:48UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    Step Name:  terminate-3
    """,
    """
    The following error has been reported at
    August 27 2024 00:16:43UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 3006c145-bd8a-490d-9ad0-368faf01828d
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 27 2024 02:08:49UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    Step Name:  checkout-1
    """,
    """
    The following error has been reported at
    August 27 2024 05:33:02UTC from one of your Tray.io integrations: 100.00%  ( 432/ 432) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 87432b18-50e9-466e-b413-1d67ae88b604
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a57e604e-3669-4ff6-ac4e-b0558b216f30
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 27 2024 09:00:03UTC from one of your Tray.io integrations: 100.00%  ( 1/ 1) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: a8b12d30-fa51-4fb1-a56c-d15197f2d0ff
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 3a8117c7-0607-4c84-b638-1ac652f2586c
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 27 2024 09:54:01UTC from one of your Tray.io integrations: 82.57%  ( 1350/ 1635) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fab4769d-31ec-49e5-8a98-200854a71eaa
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 27 2024 11:24:50UTC from one of your Tray.io integrations: Failed to reference: $.steps.stripe-1.metadata: This step failed. To access its error output, you'll need to refer to it by '$.errors.<name>' reference.
    Bellow are relevant details of error:
    Solution Instance ID: fab4769d-31ec-49e5-8a98-200854a71eaa
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 5f5f53de-00bd-4d75-988c-ac38d659ebb0
    Workflow Title: StripeDisputeToSiftChargeback
    Step Name:  script-1
    """,
    """
    The following error has been reported at
    August 27 2024 11:56:20UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 650dcdf4-b498-4638-acb5-67f5aeaa7349
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 2cfba886-611b-41c5-a442-0be625f7dd78
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 27 2024 12:12:02UTC from one of your Tray.io integrations: 100.00%  ( 158/ 158) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 693668a4-5787-4d9a-8677-28da5c481049
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: ebda89e5-64c0-4987-af27-095fa076a2bb
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 27 2024 15:06:54UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 472fafc5-2f7e-422f-8eee-448c3c257b6e
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: db8ac78b-049a-4e2b-b145-1f7a3610165f
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 27 2024 15:35:37UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: bd1b6b84-4a4d-4f7b-ac65-123f997df551
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: a10a2ecc-d06b-4cbc-a05b-fdcd71f1cffa
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 27 2024 18:10:03UTC from one of your Tray.io integrations: no matching public key
    Bellow are relevant details of error:
    Solution Instance ID: cb6eae2d-2cec-4044-9901-71b533912e4e
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 4e2c50d1-83f8-4ab4-8d46-9285e7ed1049
    Workflow Title: BraintreeDisputeToSiftChargeback
    Step Name:  trigger
    """,
    """
    The following error has been reported at
    August 27 2024 19:40:02UTC from one of your Tray.io integrations: 2.68%  ( 57/ 2126) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 5c458ce5-505b-4425-9138-38ad67099816
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 27 2024 19:56:02UTC from one of your Tray.io integrations: 71.46%  ( 303/ 424) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fd662297-e73b-4148-9f66-dd585b5e1db8
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a446880c-742b-4b01-b2f5-20fcc5359a64
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 27 2024 20:18:01UTC from one of your Tray.io integrations: 100.00%  ( 7/ 7) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 514220e6-6dfd-4f37-8028-fe946b91016e
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 39eb56f2-76de-427a-94dd-f7d9465856fe
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 28 2024 00:05:16UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 28 2024 00:22:11UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 3006c145-bd8a-490d-9ad0-368faf01828d
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 28 2024 01:07:18UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.notificationItems[0].NotificationRequestItem in property: 'object' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: 5d447912-3d3a-47d4-bae8-2396fadd14e0
    Solution ID: 83c60f1e-0ed8-4832-96d7-5ef51980f6a8
    Workflow ID: 9aa6999e-28c6-4620-9b69-9894e8519009
    Workflow Title: Adyen <> Sift Chargeback Connector
    Step Name:  object-helpers-1
    """,
    """
    The following error has been reported at
    August 28 2024 02:05:25UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    Step Name:  checkout-1
    """,
    """
    The following error has been reported at
    August 28 2024 05:33:02UTC from one of your Tray.io integrations: 100.00%  ( 500/ 500) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 87432b18-50e9-466e-b413-1d67ae88b604
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a57e604e-3669-4ff6-ac4e-b0558b216f30
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 28 2024 09:00:04UTC from one of your Tray.io integrations: 100.00%  ( 13/ 13) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: a8b12d30-fa51-4fb1-a56c-d15197f2d0ff
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 3a8117c7-0607-4c84-b638-1ac652f2586c
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 28 2024 09:54:01UTC from one of your Tray.io integrations: 83.13%  ( 1296/ 1559) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fab4769d-31ec-49e5-8a98-200854a71eaa
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 28 2024 12:12:03UTC from one of your Tray.io integrations: 100.00%  ( 17/ 17) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 693668a4-5787-4d9a-8677-28da5c481049
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: ebda89e5-64c0-4987-af27-095fa076a2bb
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 28 2024 14:20:26UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 650dcdf4-b498-4638-acb5-67f5aeaa7349
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 2cfba886-611b-41c5-a442-0be625f7dd78
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 28 2024 14:42:02UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 472fafc5-2f7e-422f-8eee-448c3c257b6e
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: db8ac78b-049a-4e2b-b145-1f7a3610165f
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 28 2024 17:05:03UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: ed15f9cd-4b0d-49e8-8a65-93f527aa3518
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 505da9bc-2fbe-483d-8535-c533524179e4
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 28 2024 19:40:01UTC from one of your Tray.io integrations: 2.75%  ( 57/ 2074) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 5c458ce5-505b-4425-9138-38ad67099816
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 28 2024 19:56:01UTC from one of your Tray.io integrations: 61.33%  ( 203/ 331) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fd662297-e73b-4148-9f66-dd585b5e1db8
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a446880c-742b-4b01-b2f5-20fcc5359a64
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 28 2024 20:18:01UTC from one of your Tray.io integrations: 100.00%  ( 8/ 8) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 514220e6-6dfd-4f37-8028-fe946b91016e
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 39eb56f2-76de-427a-94dd-f7d9465856fe
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 29 2024 00:04:07UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 29 2024 00:15:29UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    Step Name:  terminate-3
    """,
    """
    The following error has been reported at
    August 29 2024 00:56:04UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 3006c145-bd8a-490d-9ad0-368faf01828d
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 29 2024 02:03:55UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    Step Name:  checkout-1
    """,
    """
    The following error has been reported at
    August 29 2024 05:33:02UTC from one of your Tray.io integrations: 100.00%  ( 442/ 442) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 87432b18-50e9-466e-b413-1d67ae88b604
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a57e604e-3669-4ff6-ac4e-b0558b216f30
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 29 2024 09:00:03UTC from one of your Tray.io integrations: 100.00%  ( 3/ 3) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: a8b12d30-fa51-4fb1-a56c-d15197f2d0ff
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 3a8117c7-0607-4c84-b638-1ac652f2586c
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 29 2024 09:54:01UTC from one of your Tray.io integrations: 85.56%  ( 1464/ 1711) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fab4769d-31ec-49e5-8a98-200854a71eaa
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 29 2024 12:12:01UTC from one of your Tray.io integrations: 100.00%  ( 1/ 1) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 693668a4-5787-4d9a-8677-28da5c481049
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: ebda89e5-64c0-4987-af27-095fa076a2bb
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 29 2024 12:25:12UTC from one of your Tray.io integrations: Looks like the API is currently unavailable. Please check the service status of the API provider.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    Step Name:  checkout-1
    """,
    """
    The following error has been reported at
    August 29 2024 15:04:34UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 472fafc5-2f7e-422f-8eee-448c3c257b6e
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: db8ac78b-049a-4e2b-b145-1f7a3610165f
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 29 2024 16:58:52UTC from one of your Tray.io integrations: Reference: $.errors.zendesk-2.response.body in property: 'body' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: 8ee063df-60ab-437b-86d1-f7b4022fe31b
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 8794305c-d57b-4a95-a4a9-6822412f07d7
    Workflow Title: Zendesk List Tickets
    Step Name:  trigger-reply-6
    """,
    """
    The following error has been reported at
    August 29 2024 19:40:01UTC from one of your Tray.io integrations: 4.84%  ( 80/ 1653) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 5c458ce5-505b-4425-9138-38ad67099816
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 29 2024 19:56:02UTC from one of your Tray.io integrations: 66.16%  ( 131/ 198) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: fd662297-e73b-4148-9f66-dd585b5e1db8
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a446880c-742b-4b01-b2f5-20fcc5359a64
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 29 2024 20:18:01UTC from one of your Tray.io integrations: 100.00%  ( 12/ 12) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 514220e6-6dfd-4f37-8028-fe946b91016e
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 39eb56f2-76de-427a-94dd-f7d9465856fe
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 30 2024 00:01:01UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 30 2024 00:42:20UTC from one of your Tray.io integrations: Cannot read properties of undefined (reading 'id')
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 30 2024 02:05:41UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    Step Name:  checkout-1
    """,
    """
    The following error has been reported at
    August 30 2024 03:07:13UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    Step Name:  terminate-3
    """,
    """
    The following error has been reported at
    August 30 2024 03:42:01UTC from one of your Tray.io integrations: 100.00%  ( 1/ 1) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 689b5e27-2e91-4e78-bf0d-f6b3272cdf95
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 5068265c-3437-4502-8dda-0f8f7a5a595d
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 30 2024 05:33:02UTC from one of your Tray.io integrations: 100.00%  ( 653/ 653) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 87432b18-50e9-466e-b413-1d67ae88b604
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: a57e604e-3669-4ff6-ac4e-b0558b216f30
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
Alert was triggered 93 times in last 24 hours.
Details:
solution_instance_id:21145dbe-2efd-4c1a-a38d-be5f6c95f16c
workflow_id: 8792638e-cf97-4a1d-868c-b2e95837796a
workflow_title: BraintreeDisputeToSiftChargeback
message: POST Request returned non-200 and is not a rate limit
""",
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:514220e6-6dfd-4f37-8028-fe946b91016e
    workflow_id: 39eb56f2-76de-427a-94dd-f7d9465856fe
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 10/ 10) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 22 times in last 24 hours.
    Details:
    solution_instance_id:56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    workflow_id: 3006c145-bd8a-490d-9ad0-368faf01828d
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:64c55a37-ac6d-4681-adeb-86f1c11cd7e1
    workflow_id: 20faa700-2365-414c-837b-b453a0a41391
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 2/ 2) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:693668a4-5787-4d9a-8677-28da5c481049
    workflow_id: ebda89e5-64c0-4987-af27-095fa076a2bb
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 48/ 48) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:87432b18-50e9-466e-b413-1d67ae88b604
    workflow_id: a57e604e-3669-4ff6-ac4e-b0558b216f30
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 282/ 282) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 150 times in last 24 hours.
    Details:
    solution_instance_id:9258832c-1174-42f0-adbf-9366502c4ef0
    workflow_id: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    workflow_title: CheckoutDisputeEventsHandling
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 641 times in last 24 hours.
    Details:
    solution_instance_id:d43e44f3-78eb-4d85-b839-823037933c73
    workflow_id: 76722d41-8420-4f75-90c0-b45b501148f4
    workflow_title: chargeback.com chargeback_ingestion
    message: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    workflow_id: 5c458ce5-505b-4425-9138-38ad67099816
    workflow_title: Stripe Periodic Alerting
    message: 2.31%  ( 29/ 1254) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fab4769d-31ec-49e5-8a98-200854a71eaa
    workflow_id: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    workflow_title: Stripe Periodic Alerting
    message: 80.47%  ( 758/ 942) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fd662297-e73b-4148-9f66-dd585b5e1db8
    workflow_id: a446880c-742b-4b01-b2f5-20fcc5359a64
    workflow_title: Stripe Periodic Alerting
    message: 60.49%  ( 49/ 81) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 78 times in last 24 hours.
    Details:
    solution_instance_id:21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    workflow_id: 8792638e-cf97-4a1d-868c-b2e95837796a
    workflow_title: BraintreeDisputeToSiftChargeback
    message: POST Request returned non-200 and is not a rate limit
    """,
    """
    Alert was triggered 2 times in last 24 hours.
    Details:
    solution_instance_id:472fafc5-2f7e-422f-8eee-448c3c257b6e
    workflow_id: db8ac78b-049a-4e2b-b145-1f7a3610165f
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:514220e6-6dfd-4f37-8028-fe946b91016e
    workflow_id: 39eb56f2-76de-427a-94dd-f7d9465856fe
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 5/ 5) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:5cd14ea0-bfdb-477c-9ff4-6667f2887d89
    workflow_id: f1071e14-038c-4cb7-a158-114a00d77b05
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:64c55a37-ac6d-4681-adeb-86f1c11cd7e1
    workflow_id: 20faa700-2365-414c-837b-b453a0a41391
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 1/ 1) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:693668a4-5787-4d9a-8677-28da5c481049
    workflow_id: ebda89e5-64c0-4987-af27-095fa076a2bb
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 16/ 16) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:87432b18-50e9-466e-b413-1d67ae88b604
    workflow_id: a57e604e-3669-4ff6-ac4e-b0558b216f30
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 16/ 16) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 81 times in last 24 hours.
    Details:
    solution_instance_id:9258832c-1174-42f0-adbf-9366502c4ef0
    workflow_id: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    workflow_title: CheckoutDisputeEventsHandling
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:cb6eae2d-2cec-4044-9901-71b533912e4e
    workflow_id: 4e2c50d1-83f8-4ab4-8d46-9285e7ed1049
    workflow_title: BraintreeDisputeToSiftChargeback
    message: no matching public key
    """,
    """
    Alert was triggered 840 times in last 24 hours.
    Details:
    solution_instance_id:d43e44f3-78eb-4d85-b839-823037933c73
    workflow_id: 76722d41-8420-4f75-90c0-b45b501148f4
    workflow_title: chargeback.com chargeback_ingestion
    message: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    workflow_id: 5c458ce5-505b-4425-9138-38ad67099816
    workflow_title: Stripe Periodic Alerting
    message: 3.75%  ( 9/ 240) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:df76e74c-c171-4fc9-9691-982a0f7b2163
    workflow_id: 7ba2a08d-e540-4422-a117-20b84b2e99bf
    workflow_title: Stripe Periodic Alerting
    message: 33.33%  ( 1/ 3) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fab4769d-31ec-49e5-8a98-200854a71eaa
    workflow_id: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    workflow_title: Stripe Periodic Alerting
    message: 83.77%  ( 805/ 961) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fd662297-e73b-4148-9f66-dd585b5e1db8
    workflow_id: a446880c-742b-4b01-b2f5-20fcc5359a64
    workflow_title: Stripe Periodic Alerting
    message: 58.33%  ( 28/ 48) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 199 times in last 24 hours.
    Details:
    solution_instance_id:21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    workflow_id: 8792638e-cf97-4a1d-868c-b2e95837796a
    workflow_title: BraintreeDisputeToSiftChargeback
    message: POST Request returned non-200 and is not a rate limit
    """,
    """
    Alert was triggered 193 times in last 24 hours.
    Details:
    solution_instance_id:472fafc5-2f7e-422f-8eee-448c3c257b6e
    workflow_id: db8ac78b-049a-4e2b-b145-1f7a3610165f
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:472fafc5-2f7e-422f-8eee-448c3c257b6e
    workflow_id: db8ac78b-049a-4e2b-b145-1f7a3610165f
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:514220e6-6dfd-4f37-8028-fe946b91016e
    workflow_id: 39eb56f2-76de-427a-94dd-f7d9465856fe
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 2/ 2) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 84 times in last 24 hours.
    Details:
    solution_instance_id:56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    workflow_id: 3006c145-bd8a-490d-9ad0-368faf01828d
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 6 times in last 24 hours.
    Details:
    solution_instance_id:5cd14ea0-bfdb-477c-9ff4-6667f2887d89
    workflow_id: f1071e14-038c-4cb7-a158-114a00d77b05
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 98 times in last 24 hours.
    Details:
    solution_instance_id:650dcdf4-b498-4638-acb5-67f5aeaa7349
    workflow_id: 2cfba886-611b-41c5-a442-0be625f7dd78
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:650dcdf4-b498-4638-acb5-67f5aeaa7349
    workflow_id: 2cfba886-611b-41c5-a442-0be625f7dd78
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:689b5e27-2e91-4e78-bf0d-f6b3272cdf95
    workflow_id: 5068265c-3437-4502-8dda-0f8f7a5a595d
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 1/ 1) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:693668a4-5787-4d9a-8677-28da5c481049
    workflow_id: ebda89e5-64c0-4987-af27-095fa076a2bb
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 9/ 9) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:87432b18-50e9-466e-b413-1d67ae88b604
    workflow_id: a57e604e-3669-4ff6-ac4e-b0558b216f30
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 8/ 8) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 2 times in last 24 hours.
    Details:
    solution_instance_id:8ee063df-60ab-437b-86d1-f7b4022fe31b
    workflow_id: 8794305c-d57b-4a95-a4a9-6822412f07d7
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 195 times in last 24 hours.
    Details:
    solution_instance_id:9258832c-1174-42f0-adbf-9366502c4ef0
    workflow_id: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    workflow_title: CheckoutDisputeEventsHandling
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:a8a3e5cd-0b55-4821-81a7-ae0639ff353b
    workflow_id: f152186c-5089-4bdd-aac4-0edd8e36a446
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:a8b12d30-fa51-4fb1-a56c-d15197f2d0ff
    workflow_id: 3a8117c7-0607-4c84-b638-1ac652f2586c
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 2/ 2) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:af9e38cd-5952-4340-a0ef-5e0f4b7f370d
    workflow_id: 8f2b1bc1-a213-406e-9621-ecf573a106b0
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:bd1b6b84-4a4d-4f7b-ac65-123f997df551
    workflow_id: a10a2ecc-d06b-4cbc-a05b-fdcd71f1cffa
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:cb6eae2d-2cec-4044-9901-71b533912e4e
    workflow_id: 4e2c50d1-83f8-4ab4-8d46-9285e7ed1049
    workflow_title: BraintreeDisputeToSiftChargeback
    message: no matching public key
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:d42dcf74-21c8-42f9-bdc1-eeacbe3f5396
    workflow_id: cb1d256a-2b78-4292-8f57-3923526146f9
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 11 times in last 24 hours.
    Details:
    solution_instance_id:d43e44f3-78eb-4d85-b839-823037933c73
    workflow_id: 76722d41-8420-4f75-90c0-b45b501148f4
    workflow_title: chargeback.com chargeback_ingestion
    message: Cannot read properties of undefined (reading 'id')
    """,
    """
    Alert was triggered 8 times in last 24 hours.
    Details:
    solution_instance_id:d43e44f3-78eb-4d85-b839-823037933c73
    workflow_id: 76722d41-8420-4f75-90c0-b45b501148f4
    workflow_title: chargeback.com chargeback_ingestion
    message: Reference: $.steps.trigger.body.data.attributes in property: 'object' did not resolve to any value.
    """,
    """
    Alert was triggered 12931 times in last 24 hours.
    Details:
    solution_instance_id:d43e44f3-78eb-4d85-b839-823037933c73
    workflow_id: 76722d41-8420-4f75-90c0-b45b501148f4
    workflow_title: chargeback.com chargeback_ingestion
    message: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    workflow_id: 5c458ce5-505b-4425-9138-38ad67099816
    workflow_title: Stripe Periodic Alerting
    message: 4.24%  ( 50/ 1180) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fab4769d-31ec-49e5-8a98-200854a71eaa
    workflow_id: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    workflow_title: Stripe Periodic Alerting
    message: 80.30%  ( 856/ 1066) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fd662297-e73b-4148-9f66-dd585b5e1db8
    workflow_id: a446880c-742b-4b01-b2f5-20fcc5359a64
    workflow_title: Stripe Periodic Alerting
    message: 45.59%  ( 93/ 204) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 268 times in last 24 hours.
    Details:
    solution_instance_id:21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    workflow_id: 8792638e-cf97-4a1d-868c-b2e95837796a
    workflow_title: BraintreeDisputeToSiftChargeback
    message: POST Request returned non-200 and is not a rate limit
    """,
    """
    Alert was triggered 2 times in last 24 hours.
    Details:
    solution_instance_id:2dc6319b-6ac9-4804-aab0-7734ec5358b7
    workflow_id: 51e1cf0e-2230-46fe-b129-bb82453ddc20
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 180 times in last 24 hours.
    Details:
    solution_instance_id:472fafc5-2f7e-422f-8eee-448c3c257b6e
    workflow_id: db8ac78b-049a-4e2b-b145-1f7a3610165f
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:514220e6-6dfd-4f37-8028-fe946b91016e
    workflow_id: 39eb56f2-76de-427a-94dd-f7d9465856fe
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 7/ 7) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 55 times in last 24 hours.
    Details:
    solution_instance_id:56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    workflow_id: 3006c145-bd8a-490d-9ad0-368faf01828d
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:64c55a37-ac6d-4681-adeb-86f1c11cd7e1
    workflow_id: 20faa700-2365-414c-837b-b453a0a41391
    workflow_title: Stripe Periodic Alerting
    message: 66.67%  ( 2/ 3) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 292 times in last 24 hours.
    Details:
    solution_instance_id:650dcdf4-b498-4638-acb5-67f5aeaa7349
    workflow_id: 2cfba886-611b-41c5-a442-0be625f7dd78
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:693668a4-5787-4d9a-8677-28da5c481049
    workflow_id: ebda89e5-64c0-4987-af27-095fa076a2bb
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 158/ 158) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:87432b18-50e9-466e-b413-1d67ae88b604
    workflow_id: a57e604e-3669-4ff6-ac4e-b0558b216f30
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 432/ 432) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 291 times in last 24 hours.
    Details:
    solution_instance_id:9258832c-1174-42f0-adbf-9366502c4ef0
    workflow_id: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    workflow_title: CheckoutDisputeEventsHandling
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:a8b12d30-fa51-4fb1-a56c-d15197f2d0ff
    workflow_id: 3a8117c7-0607-4c84-b638-1ac652f2586c
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 1/ 1) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:b24a04e0-9e2b-4eaf-ae41-cf95cfd26ad0
    workflow_id: 179f3bd6-b558-4062-bd41-5e21e3571fed
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 2 times in last 24 hours.
    Details:
    solution_instance_id:bd1b6b84-4a4d-4f7b-ac65-123f997df551
    workflow_id: a10a2ecc-d06b-4cbc-a05b-fdcd71f1cffa
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:cb6eae2d-2cec-4044-9901-71b533912e4e
    workflow_id: 4e2c50d1-83f8-4ab4-8d46-9285e7ed1049
    workflow_title: BraintreeDisputeToSiftChargeback
    message: no matching public key
    """,
    """
    Alert was triggered 2 times in last 24 hours.
    Details:
    solution_instance_id:d42dcf74-21c8-42f9-bdc1-eeacbe3f5396
    workflow_id: cb1d256a-2b78-4292-8f57-3923526146f9
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1854 times in last 24 hours.
    Details:
    solution_instance_id:d43e44f3-78eb-4d85-b839-823037933c73
    workflow_id: 76722d41-8420-4f75-90c0-b45b501148f4
    workflow_title: chargeback.com chargeback_ingestion
    message: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    workflow_id: 5c458ce5-505b-4425-9138-38ad67099816
    workflow_title: Stripe Periodic Alerting
    message: 2.68%  ( 57/ 2126) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 2 times in last 24 hours.
    Details:
    solution_instance_id:ed15f9cd-4b0d-49e8-8a65-93f527aa3518
    workflow_id: 505da9bc-2fbe-483d-8535-c533524179e4
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fab4769d-31ec-49e5-8a98-200854a71eaa
    workflow_id: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    workflow_title: Stripe Periodic Alerting
    message: 82.57%  ( 1350/ 1635) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fab4769d-31ec-49e5-8a98-200854a71eaa
    workflow_id: 5f5f53de-00bd-4d75-988c-ac38d659ebb0
    workflow_title: StripeDisputeToSiftChargeback
    message: Failed to reference: $.steps.stripe-1.metadata: This step failed. To access its error output, you'll need to refer to it by '$.errors.<name>' reference.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fd662297-e73b-4148-9f66-dd585b5e1db8
    workflow_id: a446880c-742b-4b01-b2f5-20fcc5359a64
    workflow_title: Stripe Periodic Alerting
    message: 71.46%  ( 303/ 424) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 144 times in last 24 hours.
    Details:
    solution_instance_id:21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    workflow_id: 8792638e-cf97-4a1d-868c-b2e95837796a
    workflow_title: BraintreeDisputeToSiftChargeback
    message: POST Request returned non-200 and is not a rate limit
    """,
    """
    Alert was triggered 137 times in last 24 hours.
    Details:
    solution_instance_id:472fafc5-2f7e-422f-8eee-448c3c257b6e
    workflow_id: db8ac78b-049a-4e2b-b145-1f7a3610165f
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:514220e6-6dfd-4f37-8028-fe946b91016e
    workflow_id: 39eb56f2-76de-427a-94dd-f7d9465856fe
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 8/ 8) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 123 times in last 24 hours.
    Details:
    solution_instance_id:56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    workflow_id: 3006c145-bd8a-490d-9ad0-368faf01828d
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    workflow_id: 3006c145-bd8a-490d-9ad0-368faf01828d
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:5d447912-3d3a-47d4-bae8-2396fadd14e0
    workflow_id: 9aa6999e-28c6-4620-9b69-9894e8519009
    workflow_title: Adyen <> Sift Chargeback Connector
    message: Reference: $.steps.trigger.body.notificationItems[0].NotificationRequestItem in property: 'object' did not resolve to any value.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:64c55a37-ac6d-4681-adeb-86f1c11cd7e1
    workflow_id: 20faa700-2365-414c-837b-b453a0a41391
    workflow_title: Stripe Periodic Alerting
    message: 92.59%  ( 25/ 27) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 60 times in last 24 hours.
    Details:
    solution_instance_id:650dcdf4-b498-4638-acb5-67f5aeaa7349
    workflow_id: 2cfba886-611b-41c5-a442-0be625f7dd78
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:693668a4-5787-4d9a-8677-28da5c481049
    workflow_id: ebda89e5-64c0-4987-af27-095fa076a2bb
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 17/ 17) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:87432b18-50e9-466e-b413-1d67ae88b604
    workflow_id: a57e604e-3669-4ff6-ac4e-b0558b216f30
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 500/ 500) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 342 times in last 24 hours.
    Details:
    solution_instance_id:9258832c-1174-42f0-adbf-9366502c4ef0
    workflow_id: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    workflow_title: CheckoutDisputeEventsHandling
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:a8a3e5cd-0b55-4821-81a7-ae0639ff353b
    workflow_id: f152186c-5089-4bdd-aac4-0edd8e36a446
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:a8b12d30-fa51-4fb1-a56c-d15197f2d0ff
    workflow_id: 3a8117c7-0607-4c84-b638-1ac652f2586c
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 13/ 13) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:bd1b6b84-4a4d-4f7b-ac65-123f997df551
    workflow_id: a10a2ecc-d06b-4cbc-a05b-fdcd71f1cffa
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1979 times in last 24 hours.
    Details:
    solution_instance_id:d43e44f3-78eb-4d85-b839-823037933c73
    workflow_id: 76722d41-8420-4f75-90c0-b45b501148f4
    workflow_title: chargeback.com chargeback_ingestion
    message: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    workflow_id: 5c458ce5-505b-4425-9138-38ad67099816
    workflow_title: Stripe Periodic Alerting
    message: 2.75%  ( 57/ 2074) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:df76e74c-c171-4fc9-9691-982a0f7b2163
    workflow_id: 7ba2a08d-e540-4422-a117-20b84b2e99bf
    workflow_title: Stripe Periodic Alerting
    message: 50.00%  ( 1/ 2) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 3 times in last 24 hours.
    Details:
    solution_instance_id:ed15f9cd-4b0d-49e8-8a65-93f527aa3518
    workflow_id: 505da9bc-2fbe-483d-8535-c533524179e4
    workflow_title: Zendesk List Tickets
    message: Too many requests have been made in the given timeframe.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fab4769d-31ec-49e5-8a98-200854a71eaa
    workflow_id: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    workflow_title: Stripe Periodic Alerting
    message: 83.13%  ( 1296/ 1559) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fd662297-e73b-4148-9f66-dd585b5e1db8
    workflow_id: a446880c-742b-4b01-b2f5-20fcc5359a64
    workflow_title: Stripe Periodic Alerting
    
    """,
    """
    Alert was triggered 176 times in last 24 hours.
    Details:
    solution_instance_id:21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    workflow_id: 8792638e-cf97-4a1d-868c-b2e95837796a
    workflow_title: BraintreeDisputeToSiftChargeback
    message: POST Request returned non-200 and is not a rate limit
    """,
    """
    Alert was triggered 128 times in last 24 hours.
    Details:
    solution_instance_id:472fafc5-2f7e-422f-8eee-448c3c257b6e
    workflow_id: db8ac78b-049a-4e2b-b145-1f7a3610165f
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:514220e6-6dfd-4f37-8028-fe946b91016e
    workflow_id: 39eb56f2-76de-427a-94dd-f7d9465856fe
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 12/ 12) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 103 times in last 24 hours.
    Details:
    solution_instance_id:56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    workflow_id: 3006c145-bd8a-490d-9ad0-368faf01828d
    workflow_title: Zendesk List Tickets
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:64c55a37-ac6d-4681-adeb-86f1c11cd7e1
    workflow_id: 20faa700-2365-414c-837b-b453a0a41391
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 2/ 2) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:693668a4-5787-4d9a-8677-28da5c481049
    workflow_id: ebda89e5-64c0-4987-af27-095fa076a2bb
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 1/ 1) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:87432b18-50e9-466e-b413-1d67ae88b604
    workflow_id: a57e604e-3669-4ff6-ac4e-b0558b216f30
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 442/ 442) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:8ee063df-60ab-437b-86d1-f7b4022fe31b
    workflow_id: 8794305c-d57b-4a95-a4a9-6822412f07d7
    workflow_title: Zendesk List Tickets
    message: Reference: $.errors.zendesk-2.response.body in property: 'body' did not resolve to any value.
    """,
    """
    Alert was triggered 341 times in last 24 hours.
    Details:
    solution_instance_id:9258832c-1174-42f0-adbf-9366502c4ef0
    workflow_id: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    workflow_title: CheckoutDisputeEventsHandling
    message: Forbidden. Check you have the appropriate permissions to access this resource.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:9258832c-1174-42f0-adbf-9366502c4ef0
    workflow_id: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    workflow_title: CheckoutDisputeEventsHandling
    message: Looks like the API is currently unavailable. Please check the service status of the API provider.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:a8b12d30-fa51-4fb1-a56c-d15197f2d0ff
    workflow_id: 3a8117c7-0607-4c84-b638-1ac652f2586c
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 3/ 3) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 3060 times in last 24 hours.
    Details:
    solution_instance_id:d43e44f3-78eb-4d85-b839-823037933c73
    workflow_id: 76722d41-8420-4f75-90c0-b45b501148f4
    workflow_title: chargeback.com chargeback_ingestion
    message: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:ddc98744-8f33-45c4-b9d4-a984ef79fa4d
    workflow_id: 5c458ce5-505b-4425-9138-38ad67099816
    workflow_title: Stripe Periodic Alerting
    message: 4.84%  ( 80/ 1653) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:df76e74c-c171-4fc9-9691-982a0f7b2163
    workflow_id: 7ba2a08d-e540-4422-a117-20b84b2e99bf
    workflow_title: Stripe Periodic Alerting
    message: 100.00%  ( 23/ 23) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fab4769d-31ec-49e5-8a98-200854a71eaa
    workflow_id: 3c9080fd-d6f1-45a2-b008-dc38af9f96b9
    workflow_title: Stripe Periodic Alerting
    message: 85.56%  ( 1464/ 1711) disputes are without identifiers in last 24 hours
    """,
    """
    Alert was triggered 1 times in last 24 hours.
    Details:
    solution_instance_id:fd662297-e73b-4148-9f66-dd585b5e1db8
    workflow_id: a446880c-742b-4b01-b2f5-20fcc5359a64
    workflow_title: Stripe Periodic Alerting
    message: 66.16%  ( 131/ 198) disputes are without identifiers in last 24 hours
    """,
    """
The following error has been reported at
August 25 2024 09:55:01UTC from one of your Tray.io integrations: 33.33%  ( 1/ 3) disputes are without identifiers in last 24 hours
Bellow are relevant details of error:
Solution Instance ID: df76e74c-c171-4fc9-9691-982a0f7b2163
Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
Workflow ID: 7ba2a08d-e540-4422-a117-20b84b2e99bf
Workflow Title: Stripe Periodic Alerting
Step Name:  terminate-1
""",
    """
    The following error has been reported at
    August 25 2024 09:56:02UTC from one of your Tray.io integrations: 100.00%  ( 1/ 1) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 64c55a37-ac6d-4681-adeb-86f1c11cd7e1
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 20faa700-2365-414c-837b-b453a0a41391
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 26 2024 00:05:43UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:42UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:43UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:43UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:43UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:44UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:43UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:44UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:44UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:44UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 26 2024 00:05:44UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    Step Name:  terminate-3
    """,
    """
    The following error has been reported at
    August 26 2024 01:46:42UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 26 2024 15:02:26UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: 650dcdf4-b498-4638-acb5-67f5aeaa7349
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 2cfba886-611b-41c5-a442-0be625f7dd78
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-1
    August 26 2024 15:02:31UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: a8a3e5cd-0b55-4821-81a7-ae0639ff353b
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: f152186c-5089-4bdd-aac4-0edd8e36a446
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-7
    August 26 2024 15:02:40UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: 8ee063df-60ab-437b-86d1-f7b4022fe31b
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 8794305c-d57b-4a95-a4a9-6822412f07d7
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-1
    August 26 2024 15:02:58UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: af9e38cd-5952-4340-a0ef-5e0f4b7f370d
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 8f2b1bc1-a213-406e-9621-ecf573a106b0
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-1
    August 26 2024 15:03:29UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: 472fafc5-2f7e-422f-8eee-448c3c257b6e
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: db8ac78b-049a-4e2b-b145-1f7a3610165f
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-1
    August 26 2024 15:03:59UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: d42dcf74-21c8-42f9-bdc1-eeacbe3f5396
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: cb1d256a-2b78-4292-8f57-3923526146f9
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-7
    August 26 2024 15:04:00UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: bd1b6b84-4a4d-4f7b-ac65-123f997df551
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: a10a2ecc-d06b-4cbc-a05b-fdcd71f1cffa
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 27 2024 00:06:48UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 27 2024 00:06:49UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 27 2024 00:06:49UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 27 2024 00:06:48UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    """
    """,
    The following error has been reported atStep Name:  terminate-3
    August 27 2024 00:09:54UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 27 2024 09:56:01UTC from one of your Tray.io integrations: 66.67%  ( 2/ 3) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 64c55a37-ac6d-4681-adeb-86f1c11cd7e1
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 20faa700-2365-414c-837b-b453a0a41391
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 27 2024 15:35:44UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: b24a04e0-9e2b-4eaf-ae41-cf95cfd26ad0
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 179f3bd6-b558-4062-bd41-5e21e3571fed
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-1
    August 27 2024 15:36:41UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: d42dcf74-21c8-42f9-bdc1-eeacbe3f5396
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: cb1d256a-2b78-4292-8f57-3923526146f9
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-1
    August 27 2024 15:36:42UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: ed15f9cd-4b0d-49e8-8a65-93f527aa3518
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 505da9bc-2fbe-483d-8535-c533524179e4
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-1
    August 27 2024 15:38:32UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: 2dc6319b-6ac9-4804-aab0-7734ec5358b7
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 51e1cf0e-2230-46fe-b129-bb82453ddc20
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 28 2024 00:08:33UTC from one of your Tray.io integrations: POST Request returned non-200 and is not a rate limit
    Bellow are relevant details of error:
    Solution Instance ID: 21145dbe-2efd-4c1a-a38d-be5f6c95f16c
    Solution ID: 1aebe5e8-10e3-4233-bade-23ad934b6ba7
    Workflow ID: 8792638e-cf97-4a1d-868c-b2e95837796a
    Workflow Title: BraintreeDisputeToSiftChargeback
    Step Name:  terminate-3
    """,
    """
    The following error has been reported at
    August 28 2024 09:55:01UTC from one of your Tray.io integrations: 50.00%  ( 1/ 2) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: df76e74c-c171-4fc9-9691-982a0f7b2163
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 7ba2a08d-e540-4422-a117-20b84b2e99bf
    Workflow Title: Stripe Periodic Alerting
    """
    """,
    The following error has been reported atStep Name:  terminate-1
    August 28 2024 09:56:01UTC from one of your Tray.io integrations: 92.59%  ( 25/ 27) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 64c55a37-ac6d-4681-adeb-86f1c11cd7e1
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 20faa700-2365-414c-837b-b453a0a41391
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 28 2024 17:06:03UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: a8a3e5cd-0b55-4821-81a7-ae0639ff353b
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: f152186c-5089-4bdd-aac4-0edd8e36a446
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-1
    August 28 2024 17:08:34UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: bd1b6b84-4a4d-4f7b-ac65-123f997df551
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: a10a2ecc-d06b-4cbc-a05b-fdcd71f1cffa
    Workflow Title: Zendesk List Tickets
    """
    """,
    The following error has been reported atStep Name:  zendesk-1
    August 28 2024 17:08:36UTC from one of your Tray.io integrations: Too many requests have been made in the given timeframe.
    Bellow are relevant details of error:
    Solution Instance ID: 56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 3006c145-bd8a-490d-9ad0-368faf01828d
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported atTray.io
    August 29 2024 02:03:55UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    """
    """,
    The following error has been reported atStep Name:  checkout-1
    August 29 2024 02:03:56UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    Step Name:  checkout-1
    """,
    """
    The following error has been reported at
    August 29 2024 09:55:02UTC from one of your Tray.io integrations: 100.00%  ( 23/ 23) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: df76e74c-c171-4fc9-9691-982a0f7b2163
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 7ba2a08d-e540-4422-a117-20b84b2e99bf
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 29 2024 09:56:01UTC from one of your Tray.io integrations: 100.00%  ( 2/ 2) disputes are without identifiers in last 24 hours
    Bellow are relevant details of error:
    Solution Instance ID: 64c55a37-ac6d-4681-adeb-86f1c11cd7e1
    Solution ID: 677dedad-8c52-40d6-99fc-782b3e43ee49
    Workflow ID: 20faa700-2365-414c-837b-b453a0a41391
    Workflow Title: Stripe Periodic Alerting
    Step Name:  terminate-1
    """,
    """
    The following error has been reported at
    August 30 2024 00:01:01UTC from one of your Tray.io integrations: Reference: $.steps.trigger.body.dispute_profile.order_transactions in property: 'variables[].value' did not resolve to any value.
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    Step Name:  script-3
    """,
    """
    The following error has been reported at
    August 30 2024 00:42:20UTC from one of your Tray.io integrations: Cannot read properties of undefined (reading 'id')
    Bellow are relevant details of error:
    Solution Instance ID: d43e44f3-78eb-4d85-b839-823037933c73
    Solution ID: a00db653-9768-46dd-a33c-31cf7bf67fe2
    Workflow ID: 76722d41-8420-4f75-90c0-b45b501148f4
    Workflow Title: chargeback.com chargeback_ingestion
    """
    """,
    The following error has been reported atStep Name:  script-3
    August 30 2024 00:43:27UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 56754e7f-e1bc-4cd6-87ca-1cd2be000b77
    Solution ID: 7ce0bcff-6bfd-4155-84e0-c33bfee17e98
    Workflow ID: 3006c145-bd8a-490d-9ad0-368faf01828d
    Workflow Title: Zendesk List Tickets
    Step Name:  zendesk-1
    """,
    """
    The following error has been reported at
    August 30 2024 02:05:41UTC from one of your Tray.io integrations: Forbidden. Check you have the appropriate permissions to access this resource.
    Bellow are relevant details of error:
    Solution Instance ID: 9258832c-1174-42f0-adbf-9366502c4ef0
    Solution ID: 9efb5c1a-79e6-4450-bf1d-99db618868aa
    Workflow ID: 9e2df3f1-9d17-4bd2-8919-2d4459044e23
    Workflow Title: CheckoutDisputeEventsHandling
    Step Name:  checkout-1
    """
]

def extract_info(text):
    # Define the regex patterns
    timestamp_pattern = 'The following error has been reported at'
    alert_pattern = r'Alert was triggered (\d+) times in last 24 hours\.'
    timestamp_error = timestamp_pattern in text
    timestamp_alert = re.search(alert_pattern, text)

    if timestamp_error:
        return extract_error_info(text)
    if timestamp_alert:
        return extract_alert_info(text)

    print(f'ERROR for {text}')

def extract_error_info(text):
    # Define the regex patterns
    timestamp_pattern = r'The following error has been reported at\n([A-Za-z]+\s\d+ \d+ \d+:\d+:\d+:\d+UTC)'
    percentage_count_pattern = r'(\d+\.\d+%)\s+\( (\d+)/ (\d+)\) disputes are without identifiers in last 24 hours'
    error_message_pattern = r'from one of your Tray.io integrations:\s*(.*)'
    solution_instance_id_pattern = r'Solution Instance ID:\s*(\S+)'
    solution_id_pattern = r'Solution ID:\s*(\S+)'
    workflow_id_pattern = r'Workflow ID:\s*(\S+)'
    workflow_title_pattern = r'Workflow Title:\s*(.+)'
    step_name_pattern = r'Step Name:\s*(.+)'

    # Extracting data using regular expressions
    timestamp = re.search(timestamp_pattern, text)
    percentage_count = re.search(percentage_count_pattern, text)
    error_message = re.search(error_message_pattern, text)
    solution_instance_id = re.search(solution_instance_id_pattern, text)
    solution_id = re.search(solution_id_pattern, text)
    workflow_id = re.search(workflow_id_pattern, text)
    workflow_title = re.search(workflow_title_pattern, text)
    step_name = re.search(step_name_pattern, text)

    # Determine if we have a percentage/count or just a generic error message
    # if percentage_count:
    #     error_message_text = percentage_count.group(0)
    #     percentage = percentage_count.group(1)
    #     count = int(percentage_count.group(2))
    #     total = int(percentage_count.group(3))
    # else:
    error_message_text = error_message.group(1) if error_message else None
    percentage = None
    count = None
    total = None

    # Process and return the results
    return {
        # 'timestamp': timestamp.group(1) if timestamp else None,
        # 'percentage': percentage,
        # 'count': count,
        # 'total': total,
        'message': error_message_text,
        'solution_instance_id': solution_instance_id.group(1) if solution_instance_id else None,
        # 'solution_id': solution_id.group(1) if solution_id else None,
        # 'workflow_id': workflow_id.group(1) if workflow_id else None,
        'workflow_title': workflow_title.group(1) if workflow_title else None,
        # 'step_name': step_name.group(1) if step_name else None
    }


def extract_alert_info(text):
    # Define the regex patterns
    alert_pattern = r'Alert was triggered (\d+) times in last 24 hours\.'
    solution_id_pattern = r'solution_instance_id:(\S+)'
    workflow_id_pattern = r'workflow_id:\s*(\S+)'
    workflow_title_pattern = r'workflow_title:\s*(.+)'
    message_pattern = r'message:\s*(.+)'

    # Extracting data using regular expressions
    alert_trigger_count = re.search(alert_pattern, text)
    solution_instance_id = re.search(solution_id_pattern, text)
    workflow_id = re.search(workflow_id_pattern, text)
    workflow_title = re.search(workflow_title_pattern, text)
    message = re.search(message_pattern, text)

    # Process and return the results
    return {
        # 'alert_trigger_count': int(alert_trigger_count.group(1)) if alert_trigger_count else None,
        'solution_instance_id': solution_instance_id.group(1) if solution_instance_id else None,
        # 'workflow_id': workflow_id.group(1) if workflow_id else None,
        'workflow_title': workflow_title.group(1) if workflow_title else None,
        'message': message.group(1) if message else None
    }


def get_ites():
    alerts = []
    for text in texts:
        info = extract_info(text)
        # for key, value in info.items():
        #     if value is None:
        #         print(text)
        #         break
            # print(f'{key}: {value}')
        alerts.append(info)
    return alerts
    #     print("Extracted Info:")
    #     for key, value in info.items():
    #         print(f'{key}: {value}')
    # print()  # Print a blank line for readability between outputs
# Extract and print information for each text
