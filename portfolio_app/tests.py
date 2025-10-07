from django.test import TestCase, Client
from django.urls import reverse
from portfolio_app.models import Portfolio, Project, Student


class PortfolioModelTest(TestCase):
    def setUp(self):
        self.portfolio = Portfolio.objects.create(
            title="Test Portfolio",
            contact_email="test@example.com",
            is_active=True,
            about="Test about section"
        )

    def test_portfolio_str(self):
        self.assertEqual(str(self.portfolio), "Test Portfolio")

    def test_portfolio_get_absolute_url(self):
        expected_url = reverse('portfolio-detail', args=[str(self.portfolio.id)])
        self.assertEqual(self.portfolio.get_absolute_url(), expected_url)

    def test_portfolio_default_is_active(self):
        portfolio = Portfolio.objects.create(
            title="Inactive Portfolio",
            contact_email="inactive@example.com"
        )
        self.assertFalse(portfolio.is_active)

    def test_portfolio_fields(self):
        self.assertEqual(self.portfolio.title, "Test Portfolio")
        self.assertEqual(self.portfolio.contact_email, "test@example.com")
        self.assertTrue(self.portfolio.is_active)
        self.assertEqual(self.portfolio.about, "Test about section")


class ProjectModelTest(TestCase):
    def setUp(self):
        self.portfolio = Portfolio.objects.create(
            title="Test Portfolio",
            contact_email="test@example.com"
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="Test project description",
            portfolio=self.portfolio
        )

    def test_project_str(self):
        self.assertEqual(str(self.project), "Test Project")

    def test_project_get_absolute_url(self):
        expected_url = reverse('project-detail', args=[str(self.project.id)])
        self.assertEqual(self.project.get_absolute_url(), expected_url)

    def test_project_portfolio_relationship(self):
        self.assertEqual(self.project.portfolio, self.portfolio)

    def test_project_cascade_delete(self):
        portfolio_id = self.portfolio.id
        project_id = self.project.id
        self.portfolio.delete()

        # Verify project was deleted when portfolio was deleted
        self.assertFalse(Project.objects.filter(id=project_id).exists())

    def test_project_fields(self):
        self.assertEqual(self.project.title, "Test Project")
        self.assertEqual(self.project.description, "Test project description")


class StudentModelTest(TestCase):
    def setUp(self):
        self.portfolio = Portfolio.objects.create(
            title="Student Portfolio",
            contact_email="student@example.com"
        )
        self.student = Student.objects.create(
            name="John Doe",
            email="john.doe@msu.edu",
            major="CSCI-BS",
            portfolio=self.portfolio
        )

    def test_student_str(self):
        self.assertEqual(str(self.student), "John Doe")

    def test_student_get_absolute_url(self):
        expected_url = reverse('student-detail', args=[str(self.student.id)])
        self.assertEqual(self.student.get_absolute_url(), expected_url)

    def test_student_portfolio_relationship(self):
        self.assertEqual(self.student.portfolio, self.portfolio)
        self.assertEqual(self.portfolio.student, self.student)

    def test_student_major_choices(self):
        valid_majors = ['CSCI-BS', 'CPEN-BS', 'BIGD-BI', 'BICS-BI', 'BISC-BI', 'CSCI-BA', 'DASE-BS']
        self.assertIn(self.student.major, valid_majors)

    def test_student_without_portfolio(self):
        student = Student.objects.create(
            name="Jane Doe",
            email="jane.doe@msu.edu",
            major="CPEN-BS"
        )
        self.assertIsNone(student.portfolio)

    def test_student_cascade_delete(self):
        portfolio_id = self.portfolio.id
        student_id = self.student.id
        self.portfolio.delete()

        # Verify student was deleted when portfolio was deleted
        self.assertFalse(Student.objects.filter(id=student_id).exists())

    def test_student_fields(self):
        self.assertEqual(self.student.name, "John Doe")
        self.assertEqual(self.student.email, "john.doe@msu.edu")
        self.assertEqual(self.student.major, "CSCI-BS")


# View Tests
class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.active_portfolio = Portfolio.objects.create(
            title="Active Portfolio",
            contact_email="active@example.com",
            is_active=True
        )
        self.inactive_portfolio = Portfolio.objects.create(
            title="Inactive Portfolio",
            contact_email="inactive@example.com",
            is_active=False
        )

    def test_index_view_status_code(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'portfolio_app/index.html')

    def test_index_view_shows_only_active_portfolios(self):
        response = self.client.get(reverse('index'))
        self.assertIn('portfolios', response.context)
        self.assertIn(self.active_portfolio, response.context['portfolios'])
        self.assertNotIn(self.inactive_portfolio, response.context['portfolios'])


class PortfolioDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.portfolio = Portfolio.objects.create(
            title="Test Portfolio",
            contact_email="test@example.com",
            is_active=True
        )
        self.student = Student.objects.create(
            name="John Doe",
            email="john.doe@msu.edu",
            major="CSCI-BS",
            portfolio=self.portfolio
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="Test description",
            portfolio=self.portfolio
        )

    def test_portfolio_detail_view_status_code(self):
        response = self.client.get(reverse('portfolio-detail', args=[self.portfolio.id]))
        self.assertEqual(response.status_code, 200)

    def test_portfolio_detail_view_not_found(self):
        response = self.client.get(reverse('portfolio-detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_portfolio_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('portfolio-detail', args=[self.portfolio.id]))
        self.assertTemplateUsed(response, 'portfolio_app/portfolio_detail.html')

    def test_portfolio_detail_view_context(self):
        response = self.client.get(reverse('portfolio-detail', args=[self.portfolio.id]))
        self.assertEqual(response.context['portfolio'], self.portfolio)
        self.assertEqual(response.context['student'], self.student)
        self.assertIn(self.project, response.context['projects'])

    def test_portfolio_detail_without_student(self):
        portfolio_no_student = Portfolio.objects.create(
            title="No Student Portfolio",
            contact_email="nostudent@example.com"
        )
        response = self.client.get(reverse('portfolio-detail', args=[portfolio_no_student.id]))
        self.assertIsNone(response.context['student'])


class PortfolioUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.portfolio = Portfolio.objects.create(
            title="Original Title",
            contact_email="original@example.com",
            is_active=False,
            about="Original about"
        )

    def test_portfolio_update_get_status_code(self):
        response = self.client.get(reverse('portfolio-update', args=[self.portfolio.id]))
        self.assertEqual(response.status_code, 200)

    def test_portfolio_update_uses_correct_template(self):
        response = self.client.get(reverse('portfolio-update', args=[self.portfolio.id]))
        self.assertTemplateUsed(response, 'portfolio_app/portfolio_form.html')

    def test_portfolio_update_post_valid_data(self):
        data = {
            'title': 'Updated Title',
            'contact_email': 'updated@example.com',
            'about': 'Updated about',
            'is_active': 'on'
        }
        response = self.client.post(reverse('portfolio-update', args=[self.portfolio.id]), data=data)
        self.assertEqual(response.status_code, 302)

        self.portfolio.refresh_from_db()
        self.assertEqual(self.portfolio.title, 'Updated Title')
        self.assertEqual(self.portfolio.contact_email, 'updated@example.com')
        self.assertEqual(self.portfolio.about, 'Updated about')
        self.assertTrue(self.portfolio.is_active)

    def test_portfolio_update_post_invalid_data(self):
        data = {
            'title': '',
            'contact_email': '',
        }
        response = self.client.post(reverse('portfolio-update', args=[self.portfolio.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio_app/portfolio_form.html')


class ProjectListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.portfolio = Portfolio.objects.create(
            title="Test Portfolio",
            contact_email="test@example.com"
        )
        self.project1 = Project.objects.create(
            title="Project 1",
            description="Description 1",
            portfolio=self.portfolio
        )
        self.project2 = Project.objects.create(
            title="Project 2",
            description="Description 2",
            portfolio=self.portfolio
        )

    def test_project_list_view_status_code(self):
        response = self.client.get(reverse('project-list', args=[self.portfolio.id]))
        self.assertEqual(response.status_code, 200)

    def test_project_list_view_uses_correct_template(self):
        response = self.client.get(reverse('project-list', args=[self.portfolio.id]))
        self.assertTemplateUsed(response, 'portfolio_app/project_list.html')

    def test_project_list_view_context(self):
        response = self.client.get(reverse('project-list', args=[self.portfolio.id]))
        self.assertEqual(response.context['portfolio'], self.portfolio)
        self.assertIn(self.project1, response.context['projects'])
        self.assertIn(self.project2, response.context['projects'])


class ProjectDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.portfolio = Portfolio.objects.create(
            title="Test Portfolio",
            contact_email="test@example.com"
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="Test description",
            portfolio=self.portfolio
        )

    def test_project_detail_view_status_code(self):
        response = self.client.get(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_project_detail_view_not_found(self):
        response = self.client.get(reverse('project-detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_project_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('project-detail', args=[self.project.id]))
        self.assertTemplateUsed(response, 'portfolio_app/project_detail.html')

    def test_project_detail_view_context(self):
        response = self.client.get(reverse('project-detail', args=[self.project.id]))
        self.assertEqual(response.context['project'], self.project)


class ProjectCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.portfolio = Portfolio.objects.create(
            title="Test Portfolio",
            contact_email="test@example.com"
        )

    def test_project_create_get_status_code(self):
        response = self.client.get(reverse('project-create', args=[self.portfolio.id]))
        self.assertEqual(response.status_code, 200)

    def test_project_create_uses_correct_template(self):
        response = self.client.get(reverse('project-create', args=[self.portfolio.id]))
        self.assertTemplateUsed(response, 'portfolio_app/project_form.html')

    def test_project_create_post_valid_data(self):
        data = {
            'title': 'New Project',
            'description': 'New project description'
        }
        response = self.client.post(reverse('project-create', args=[self.portfolio.id]), data=data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(Project.objects.filter(title='New Project').exists())
        project = Project.objects.get(title='New Project')
        self.assertEqual(project.description, 'New project description')
        self.assertEqual(project.portfolio, self.portfolio)

    def test_project_create_post_invalid_data(self):
        data = {
            'title': '',
            'description': ''
        }
        response = self.client.post(reverse('project-create', args=[self.portfolio.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio_app/project_form.html')


class ProjectUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.portfolio = Portfolio.objects.create(
            title="Test Portfolio",
            contact_email="test@example.com"
        )
        self.project = Project.objects.create(
            title="Original Title",
            description="Original description",
            portfolio=self.portfolio
        )

    def test_project_update_get_status_code(self):
        response = self.client.get(reverse('project-update', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_project_update_uses_correct_template(self):
        response = self.client.get(reverse('project-update', args=[self.project.id]))
        self.assertTemplateUsed(response, 'portfolio_app/project_form.html')

    def test_project_update_post_valid_data(self):
        data = {
            'title': 'Updated Title',
            'description': 'Updated description'
        }
        response = self.client.post(reverse('project-update', args=[self.project.id]), data=data)
        self.assertEqual(response.status_code, 302)

        self.project.refresh_from_db()
        self.assertEqual(self.project.title, 'Updated Title')
        self.assertEqual(self.project.description, 'Updated description')

    def test_project_update_post_invalid_data(self):
        data = {
            'title': '',
            'description': ''
        }
        response = self.client.post(reverse('project-update', args=[self.project.id]), data=data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'portfolio_app/project_form.html')


class ProjectDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.portfolio = Portfolio.objects.create(
            title="Test Portfolio",
            contact_email="test@example.com"
        )
        self.project = Project.objects.create(
            title="Test Project",
            description="Test description",
            portfolio=self.portfolio
        )

    def test_project_delete_get_status_code(self):
        response = self.client.get(reverse('project-delete', args=[self.project.id]))
        self.assertEqual(response.status_code, 200)

    def test_project_delete_uses_correct_template(self):
        response = self.client.get(reverse('project-delete', args=[self.project.id]))
        self.assertTemplateUsed(response, 'portfolio_app/project_confirm_delete.html')

    def test_project_delete_post(self):
        project_id = self.project.id
        response = self.client.post(reverse('project-delete', args=[self.project.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Project.objects.filter(id=project_id).exists())


class StudentListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student1 = Student.objects.create(
            name="Alice",
            email="alice@msu.edu",
            major="CSCI-BS"
        )
        self.student2 = Student.objects.create(
            name="Bob",
            email="bob@msu.edu",
            major="CPEN-BS"
        )

    def test_student_list_view_status_code(self):
        response = self.client.get(reverse('student-list'))
        self.assertEqual(response.status_code, 200)

    def test_student_list_view_uses_correct_template(self):
        response = self.client.get(reverse('student-list'))
        self.assertTemplateUsed(response, 'portfolio_app/student_list.html')

    def test_student_list_view_context(self):
        response = self.client.get(reverse('student-list'))
        self.assertIn('students', response.context)
        students = list(response.context['students'])
        self.assertEqual(students[0], self.student1)  # Alice comes before Bob
        self.assertEqual(students[1], self.student2)


class StudentDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.student = Student.objects.create(
            name="John Doe",
            email="john.doe@msu.edu",
            major="CSCI-BS"
        )

    def test_student_detail_view_status_code(self):
        response = self.client.get(reverse('student-detail', args=[self.student.id]))
        self.assertEqual(response.status_code, 200)

    def test_student_detail_view_not_found(self):
        response = self.client.get(reverse('student-detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_student_detail_view_uses_correct_template(self):
        response = self.client.get(reverse('student-detail', args=[self.student.id]))
        self.assertTemplateUsed(response, 'portfolio_app/student_detail.html')

    def test_student_detail_view_context(self):
        response = self.client.get(reverse('student-detail', args=[self.student.id]))
        self.assertEqual(response.context['student'], self.student)
