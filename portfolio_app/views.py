from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from portfolio_app.models import Portfolio, Student, Project
from django.http import HttpResponse



# Display home page with active portfolios
def index(request):
    portfolios = Portfolio.objects.filter(is_active=True)
    context = {
        'portfolios': portfolios,
    }
    return render(request, 'portfolio_app/index.html', context)


# Display portfolio details with projects
def portfolio_detail(request, id):
    portfolio = get_object_or_404(Portfolio, id=id)
    projects = Project.objects.filter(portfolio=portfolio)
    
    # Get the student associated with this portfolio
    try:
        student = portfolio.student
    except Student.DoesNotExist:
        student = None
    
    context = {
        'portfolio': portfolio,
        'projects': projects,
        'student': student,
    }
    return render(request, 'portfolio_app/portfolio_detail.html', context)


# Update portfolio information
def portfolio_update(request, id):
    portfolio = get_object_or_404(Portfolio, id=id)
    
    if request.method == 'POST':
        portfolio.title = request.POST.get('title')
        portfolio.about = request.POST.get('about')
        portfolio.contact_email = request.POST.get('contact_email')
        portfolio.is_active = request.POST.get('is_active') == 'on'
        
        # Basic validation
        if not portfolio.title or not portfolio.contact_email:
            messages.error(request, 'Title and Contact Email are required!')
            context = {'portfolio': portfolio}
            return render(request, 'portfolio_app/portfolio_form.html', context)
        
        portfolio.save()
        messages.success(request, 'Portfolio updated successfully!')
        return redirect('portfolio-detail', id=portfolio.id)
    
    context = {
        'portfolio': portfolio,
    }
    return render(request, 'portfolio_app/portfolio_form.html', context)


# Display list of projects for a portfolio
def project_list(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    projects = Project.objects.filter(portfolio=portfolio)
    context = {
        'portfolio': portfolio,
        'projects': projects,
    }
    return render(request, 'portfolio_app/project_list.html', context)


# Display project details
def project_detail(request, id):
    project = get_object_or_404(Project, id=id)
    context = {
        'project': project,
    }
    return render(request, 'portfolio_app/project_detail.html', context)


# Create a new project for a portfolio
def project_create(request, portfolio_id):
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Basic validation
        if not title or not description:
            messages.error(request, 'Title and Description are required!')
            context = {'portfolio': portfolio}
            return render(request, 'portfolio_app/project_form.html', context)
        
        project = Project(
            title=title,
            description=description,
            portfolio=portfolio
        )
        project.save()
        messages.success(request, 'Project created successfully!')
        return redirect('portfolio-detail', id=portfolio.id)
    
    context = {
        'portfolio': portfolio,
        'is_create': True,
    }
    return render(request, 'portfolio_app/project_form.html', context)


# Update an existing project
def project_update(request, id):
    project = get_object_or_404(Project, id=id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        
        # Basic validation
        if not title or not description:
            messages.error(request, 'Title and Description are required!')
            context = {
                'project': project,
                'portfolio': project.portfolio,
                'is_create': False,
            }
            return render(request, 'portfolio_app/project_form.html', context)
        
        project.title = title
        project.description = description
        project.save()
        messages.success(request, 'Project updated successfully!')
        return redirect('portfolio-detail', id=project.portfolio.id)
    
    context = {
        'project': project,
        'portfolio': project.portfolio,
        'is_create': False,
    }
    return render(request, 'portfolio_app/project_form.html', context)


# Delete a project
def project_delete(request, id):
    project = get_object_or_404(Project, id=id)
    portfolio_id = project.portfolio.id
    
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'Project deleted successfully!')
        return redirect('portfolio-detail', id=portfolio_id)
    
    context = {
        'project': project,
        'portfolio': project.portfolio,
    }
    return render(request, 'portfolio_app/project_confirm_delete.html', context)


# Display list of all students
def student_list(request):
    students = Student.objects.all().order_by('name')
    context = {
        'students': students,
    }
    return render(request, 'portfolio_app/student_list.html', context)


# Display student details
def student_detail(request, id):
    student = get_object_or_404(Student, id=id)
    context = {
        'student': student,
    }
    return render(request, 'portfolio_app/student_detail.html', context)