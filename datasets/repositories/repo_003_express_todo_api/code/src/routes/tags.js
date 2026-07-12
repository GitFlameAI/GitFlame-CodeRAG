const express = require("express");
const tagStore = require("../store/tagStore");

const router = express.Router();

router.get("/:id/tags", (req, res) => {
  res.json(tagStore.listTags(Number(req.params.id)));
});

router.post("/:id/tags", (req, res) => {
  const { tag } = req.body;
  if (!tag) {
    return res.status(400).json({ error: "tag is required" });
  }
  res.status(201).json(tagStore.addTag(Number(req.params.id), tag));
});

router.delete("/:id/tags/:tag", (req, res) => {
  const removed = tagStore.removeTag(Number(req.params.id), req.params.tag);
  res.status(removed ? 204 : 404).end();
});

module.exports = router;
