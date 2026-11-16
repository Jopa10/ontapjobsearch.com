ALTER TABLE ontap_shadow.advert_appearances
    ADD COLUMN IF NOT EXISTS source_row_position integer
    CHECK (source_row_position IS NULL OR source_row_position > 0);

COMMENT ON COLUMN ontap_shadow.advert_appearances.source_row_position IS
    '1-based position of the advert among JobG8 Job elements in the original feed XML; NULL only for historical rows imported before capture.';
