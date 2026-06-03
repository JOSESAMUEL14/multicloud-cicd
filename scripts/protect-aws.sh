#!/bin/bash
# ── AWS Protection Script ──
# Run this RIGHT AFTER creating your AWS account
# Sets up billing alerts so you never get charged unexpectedly

echo "================================================"
echo "  AWS Free Tier Protection Setup"
echo "================================================"

# Set billing alert at $1
aws budgets create-budget \
  --account-id $(aws sts get-caller-identity --query Account --output text) \
  --budget '{
    "BudgetName": "FreeTracker-1dollar",
    "BudgetLimit": {"Amount": "1","Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST"
  }' \
  --notifications-with-subscribers '[{
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80
    },
    "Subscribers": [{
      "SubscriptionType": "EMAIL",
      "Address": "Josesamueld2005@gmail.com"
    }]
  }]' 2>/dev/null && echo "✅ Alert set: Email when spending reaches $0.80" || echo "⚠️ Run this after AWS login"

echo ""
echo "================================================"
echo "  DELETE EVERYTHING CHECKLIST"
echo "  Run these commands to delete all resources:"
echo "================================================"
echo ""
echo "  1. Stop EC2:    aws ec2 stop-instances --instance-ids YOUR_ID"
echo "  2. Delete EC2:  aws ec2 terminate-instances --instance-ids YOUR_ID"
echo "  3. Delete SG:   aws ec2 delete-security-group --group-id YOUR_SG_ID"
echo "  4. Release EIP: aws ec2 release-address --allocation-id YOUR_EIP_ID"
echo "  5. Check bill:  https://console.aws.amazon.com/billing"
echo ""
echo "  OR use Terraform: terraform destroy"
echo "  This deletes EVERYTHING in one command!"
echo "================================================"
