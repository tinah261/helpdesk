from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, current_app
from flask_login import login_required, current_user
from .models import db, User, Ticket
from datetime import datetime, timezone

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    # Récupération de la version et du message dynamique depuis la configuration
    version = current_app.config.get('APP_VERSION', '1.0.0')
    message = current_app.config.get('APP_MESSAGE', 'Application HelpDesk')
    return render_template('index.html', version=version, message=message)

@main_bp.route('/health')
def health():
    version = current_app.config.get('APP_VERSION', '1.0.0')
    return jsonify({
        "status": "ok",
        "version": version
    })

@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Si l'utilisateur est admin, on le redirige vers le dashboard admin
    if current_user.is_admin():
        return redirect(url_for('main.admin_dashboard'))
        
    # Stats pour l'utilisateur connecté
    user_tickets = Ticket.query.filter_by(user_id=current_user.id)
    total_created = user_tickets.count()
    open_count = user_tickets.filter_by(status='Ouvert').count()
    resolved_count = user_tickets.filter_by(status='Résolu').count()
    
    # Derniers tickets de l'utilisateur
    recent_tickets = user_tickets.order_by(Ticket.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                           total_created=total_created,
                           open_count=open_count,
                           resolved_count=resolved_count,
                           recent_tickets=recent_tickets)

@main_bp.route('/admin/dashboard')
@login_required
def admin_dashboard():
    # Contrôle d'accès admin
    if not current_user.is_admin():
        flash("Accès refusé. Cette page est réservée aux administrateurs.", "danger")
        return redirect(url_for('main.dashboard'))
        
    # Stats globales
    total = Ticket.query.count()
    open_count = Ticket.query.filter_by(status='Ouvert').count()
    in_progress = Ticket.query.filter_by(status='En cours').count()
    resolved = Ticket.query.filter_by(status='Résolu').count()
    closed = Ticket.query.filter_by(status='Fermé').count()
    urgent = Ticket.query.filter_by(priority='Urgente').count()
    
    # Tous les tickets pour le tableau
    all_tickets = Ticket.query.order_by(Ticket.created_at.desc()).all()
    
    return render_template('admin_dashboard.html',
                           total=total,
                           open_count=open_count,
                           in_progress=in_progress,
                           resolved=resolved,
                           closed=closed,
                           urgent=urgent,
                           all_tickets=all_tickets)

@main_bp.route('/tickets')
@login_required
def tickets():
    # Filtres de recherche
    status_filter = request.args.get('status')
    priority_filter = request.args.get('priority')
    category_filter = request.args.get('category')
    
    if current_user.is_admin():
        query = Ticket.query
    else:
        query = Ticket.query.filter_by(user_id=current_user.id)
        
    if status_filter:
        query = query.filter_by(status=status_filter)
    if priority_filter:
        query = query.filter_by(priority=priority_filter)
    if category_filter:
        query = query.filter_by(category=category_filter)
        
    ticket_list = query.order_by(Ticket.created_at.desc()).all()
    
    return render_template('tickets.html', 
                           tickets=ticket_list,
                           status_filter=status_filter,
                           priority_filter=priority_filter,
                           category_filter=category_filter)

@main_bp.route('/tickets/new', methods=['GET', 'POST'])
@login_required
def create_ticket():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category = request.form.get('category')
        priority = request.form.get('priority')
        
        if not title or not description or not category or not priority:
            flash('Veuillez remplir tous les champs obligatoires.', 'danger')
            return redirect(url_for('main.create_ticket'))
            
        new_ticket = Ticket(
            title=title,
            description=description,
            category=category,
            priority=priority,
            status='Ouvert',
            user_id=current_user.id
        )
        db.session.add(new_ticket)
        db.session.commit()
        
        flash('Le ticket a été créé avec succès.', 'success')
        return redirect(url_for('main.dashboard'))
        
    return render_template('create_ticket.html')

@main_bp.route('/tickets/<int:ticket_id>', methods=['GET', 'POST'])
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    # Contrôle d'accès : seul l'admin ou le créateur du ticket peut le voir
    if not current_user.is_admin() and ticket.user_id != current_user.id:
        flash("Vous n'êtes pas autorisé à consulter ce ticket.", "danger")
        return redirect(url_for('main.dashboard'))
        
    if request.method == 'POST':
        if current_user.is_admin():
            new_status = request.form.get('status')
            new_priority = request.form.get('priority')
            admin_response = request.form.get('admin_response')
            
            if new_status:
                ticket.status = new_status
            if new_priority:
                ticket.priority = new_priority
            if admin_response is not None:
                ticket.admin_response = admin_response
                
            ticket.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            
            flash('Ticket mis à jour avec succès.', 'success')
        else:
            flash('Seul un administrateur peut modifier ce ticket.', 'danger')
            
        return redirect(url_for('main.ticket_detail', ticket_id=ticket.id))
        
    return render_template('ticket_detail.html', ticket=ticket)
