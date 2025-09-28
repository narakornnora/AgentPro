const express = require('express');
const router = express.Router();
const { protect, authorize } = require('../middleware/auth');

// @route   GET /api/v1/resource
router.get('/', (req, res) => {
  res.status(200).json({
    success: true,
    data: []
  });
});

// @route   POST /api/v1/resource
router.post('/', protect, (req, res) => {
  res.status(201).json({
    success: true,
    data: {}
  });
});

module.exports = router;
