import express from "express";

import {
  adminLogin,
  userDelete,
  userList,
  paymentList,
} from "../controllers/adminController.js";

const router = express.Router();

router.post("/admin-login", adminLogin);
router.delete("/delete-user", userDelete);
router.get("/user-list", userList);
router.get("/payment-list", paymentList);

export default router;
