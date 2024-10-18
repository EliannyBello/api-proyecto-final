from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, JobPosting, Language, Technology, Rank, post_languages, tech_knowledges

bp_job_posting = Blueprint('bp_job_posting', __name__)

@bp_job_posting.route('/job_postings', methods=['GET'])
def get_all_job_postings():
    job_postings = JobPosting.query.all()
    
    if not job_postings:
        return jsonify({"status": "error", "message": "No job postings found"}), 404
    
    print(job_postings)
    serialized_jobs = [post.serialize()for post in job_postings]
    print(serialized_jobs)
    
    return jsonify({"status": "success", "job_postings": serialized_jobs}), 200


@bp_job_posting.route('/job_postings/<int:id>', methods=['GET'])
def get_job_posting(id):
    job_posting = JobPosting.query.get(id)
    if not job_posting:
        return jsonify({"status": "error", "message": "Job posting not found"}), 404
    return jsonify({"status": "success", "job_posting": job_posting.serialize()}), 200



@bp_job_posting.route('/job_postings/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_job_posting_by_id(user_id):
    job_posting = JobPosting.query.filter_by(user_id=user_id).all()

    if not job_posting:
        return jsonify({"status": "error", "message": "Job posting not found"}), 404
    
    serialized_post = [post.serialize()for post in job_posting]

    return jsonify({"status": "success", "job_posting": serialized_post}), 200




@bp_job_posting.route('/job_postings', methods=['POST'])
@jwt_required()
def create_job_posting():
    user_id = get_jwt_identity()  
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({"status": "error", "message": "User is not authorized"}), 401

  
    title = request.json.get('title')
    description = request.json.get('description')
    payment = request.json.get('payment')
    required_time = request.json.get('required_time')
    expiration_date = request.json.get('expiration_date')
    languages = request.json.get('languages')
    technologies = request.json.get('technologies')
    rank_id = request.json.get('rank')


    if not title:
        return jsonify({"status": "error", "message": "Title is required"}), 422
    
    if not description:
        return jsonify({"status": "error", "message": "Description is required"}), 422
    
    if not payment:
        return jsonify({"status": "error", "message": "Payment is required"}), 422
    
    if not required_time:
        return jsonify({"status": "error", "message": "Time is required"}), 422
    
    if not expiration_date:
        return jsonify({"status": "error", "message": "Expiration Date is required"}), 422

    if len(languages) == 0:
        return jsonify({"status": "error", "message": "Languages is required"}), 422

    if len(technologies) == 0:
        return jsonify({"status": "error", "message": "Technology is required"}), 422

    if not rank_id:
        return jsonify({"status": "error", "message": "Rank is required"}), 422
        

    new_job_posting = JobPosting()
    new_job_posting.title=title
    new_job_posting.description=description
    new_job_posting.payment=payment
    new_job_posting.required_time=required_time
    new_job_posting.expiration_date=expiration_date
    new_job_posting.user_id=user_id
    new_job_posting.rank_id = rank_id
    

    for l in languages:
        lang = Language.query.filter_by(name = l).first()
        new_job_posting.languages.append(lang)


    for t in technologies:
        tech = Technology.query.filter_by(name = t).first()
        new_job_posting.technologies.append(tech)
        
    new_job_posting.save()

    return jsonify({"status": "success", "message": "Job posting created!", "job_posting": new_job_posting.serialize()}), 201



@bp_job_posting.route('/job_postings/<int:id>', methods=['PATCH'])
@jwt_required()
def update_job_posting(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    job_posting = JobPosting.query.get(id)

    if not job_posting:
        return jsonify({"status": "error", "message": "Job posting not found"}), 404

  
    if job_posting.user_id != user_id:
        return jsonify({"status": "error", "message": "You are not allowed to update this job posting"}), 403


    job_posting.title = request.json.get('title', job_posting.title)
    job_posting.description = request.json.get('description', job_posting.description)
    job_posting.payment = request.json.get('payment', job_posting.payment)
    job_posting.required_time = request.json.get('required_time', job_posting.required_time)
    job_posting.expiration_date = request.json.get('expiration_date', job_posting.expiration_date)
    job_posting.status_id = request.json.get('status_id', job_posting.status_id)

    job_posting.update()

    return jsonify({"status": "success", "message": "Job posting updated!", "job_posting": job_posting.serialize()}), 200


@bp_job_posting.route('/job_postings/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_job_posting(id):
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    job_posting = JobPosting.query.get(id)

    if not job_posting:
        return jsonify({"status": "error", "message": "Job posting not found"}), 404

  
    if job_posting.user_id != user_id:
        return jsonify({"status": "error", "message": "You are not allowed to delete this job posting"}), 403

    job_posting.delete()

    return jsonify({"status": "success", "message": "Job posting deleted!"}), 200
