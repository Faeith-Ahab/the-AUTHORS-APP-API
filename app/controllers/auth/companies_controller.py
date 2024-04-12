from flask import Blueprint, request, jsonify
from app.models.companies import Company  # Import Company from models
from app.extensions import db
from datetime import datetime

company = Blueprint('company', __name__, url_prefix='/api/v1/company')

@company.route('/register', methods=['POST'])
def register_company():
    try:
        # Extract data from request
        data = request.json

        # Basic input validation
        if not all([data.get(field) for field in ['name', 'origin', 'description', 'user_id', 'user_type']]):
            return jsonify({"error": "All fields are required"}), 400

# CREATING A NEW COMPANY 
        
        
        new_company = Company(
            name=data['name'],
            origin=data['origin'],
            description=data['description'],
            user_id=data['user_id'],
            user_type=data['user_type'],
           created_at=data.get('created_at', datetime.now())  # Handle optional created_at
        )

        # Add and commit to database
        db.session.add(new_company)
        db.session.commit()

        # Build response message
        return jsonify({"message": f"Company '{new_company.name}' has been registered"}), 201

    except Exception as e:
        # Handle exceptions appropriately (e.g., database errors, validation errors)
        return jsonify({"error": str(e)}), 500
    

# UPDATING COMPANIES
    

@company.route('/<int:company_id>', methods=['PUT'])
def update_company(company_id):
  try:
    # Get company object by ID
    company = Company.query.get(company_id)

    # Check if company exists
    if not company:
      return jsonify({"error": f"Company with ID {company_id} not found"}), 404

    # Extract data from request (excluding ID)
    data = request.json
    update_data = {field: data.get(field) for field in ['name', 'origin', 'description', 'user_id', 'user_type'] if field != 'id'}

    # Update company attributes
    for field, value in update_data.items():
      setattr(company, field, value)

    # Commit changes to database
    db.session.commit()

    # Build response message
    return jsonify({"message": f"Company with ID {company_id} has been updated"}), 200

  except Exception as e:
    # Handle exceptions appropriately
    return jsonify({"error": str(e)}), 500

# DELETING COMPANY

@company.route('/<int:company_id>', methods=['DELETE'])
def delete_company(company_id):
  try:
    # Get company object by ID
    company = Company.query.get(company_id)

    # Check if company exists
    if not company:
      return jsonify({"error": f"Company with ID {company_id} not found"}), 404

    # Delete the company (consider soft deletion if needed)
    db.session.delete(company)
    db.session.commit()

    # Build response message
    return jsonify({"message": f"Company with ID {company_id} has been deleted"}), 204

  except Exception as e:
    # Handle exceptions appropriately
    return jsonify({"error": str(e)}), 500


# GETTING ALL COMPANIES

@company.route('/', methods=['GET'])
def get_all_companies():
  companies = Company.query.all()

  if not companies:
      return jsonify({"message": "No companies found"}), 404  # Not Found status code

  companies_data = [company.to_dict() for company in companies]
  return jsonify(companies_data), 200