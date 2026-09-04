---
id: SR-900
title: "negative — a SpecReview with no Findings table"
type: SpecReview
analysis: base
review_set: subset
expect: mapping.missing
because: "`findings` is a required locator; a review with no findings table asserts nothing"
---
# SR-900: negative — a SpecReview with no Findings table

## Summary

An analysis that found nothing still records one row. This document records none.
