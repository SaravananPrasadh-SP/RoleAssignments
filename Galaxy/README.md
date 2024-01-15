# Galaxy Tags Migration
This repository contains the scripts and data used to migrate the tags from the old Galaxy instance to the new one.
# Goals
### Dev to Prod
Typically the classifications are production level things, the tagging would not be tested in the sense the policies might have to be tested, but the real life we may test the actions on the tag and its policies. So the part of tags that will be tested would the identification of the new tags, the resources that will be tagged are in production level event. 

Overall it should do Export Tags with dependencies and import with validation.

* Export the tag with its dependencies.
* Import the tag with validation.
* Validate the tag is imported with the policies.
* Produce error report what failed and why.

For now, lets export everything and Import, irrespective of overwriting the existing tags. Later we need to think of, 
* How to incrementally extract the tags.
* How to incrementally import tags with option to overwrite or skip.

So to test it would be,
* Create a new tag in dev Galaxy Instance.
* Assign Policies for the tag
* Migrate the tag to the prod Galaxy Instance.
* Ensure the tag is migrated with the policies.

