from django.shortcuts import render, redirect
from .models import Registration, TeamMember
from django.contrib import messages
from django.db import transaction, IntegrityError

def index(request):
    domains = [
        "Civil Engineering", "Computer Science", "Electronics & Comm.",
        "Information Tech", "Electrical & Electronics", "Mechanical Engg",
        "MBA", "MCA", "Science & Humanities"
    ]
    return render(request, 'web/index.html', {'domains': domains})

def register(request):
    if request.method == 'POST':
        print("\n--- DEBUG: Registration Attempt Started ---")
        try:
            with transaction.atomic():
                # Extract basic info
                project_title = request.POST.get('project_title')
                project_category = request.POST.get('project_category') # NEW
                print(f"DEBUG: Project Title: {project_title}, Category: {project_category}")

                if not project_category:
                     messages.error(request, "Please select a project category.")
                     return render(request, 'web/register.html')
                
                # Team Size from hidden input or calculate (let's use hidden input which is consistent with UI)
                try:
                    team_size = int(request.POST.get('team_size', 2))
                except ValueError:
                    team_size = 2
                print(f"DEBUG: Team Size: {team_size}")
                
                # Leader Details from Member 1
                leader_name = request.POST.get('member_name_1')
                leader_email = request.POST.get('member_email_1')
                leader_mobile = request.POST.get('member_mobile_1')
                
                # Validation (Min 2, Max 6) is handled nicely by UI, but good to be safe if manual post
                if team_size < 2: team_size = 2
                if team_size > 6: team_size = 6

                college_sel = request.POST.get('college_selection')
                print(f"DEBUG: College Selection: {college_sel}")
                college_other = request.POST.get('college_name_other') if college_sel == 'OTHER' else None
                
                trans_id = request.POST.get('transaction_id')
                
                # Check uniqueness manually
                if Registration.objects.filter(project_title=project_title).exists():
                    print("DEBUGGING ERROR: Project Title already exists.")
                    messages.error(request, "Project Title already exists.")
                    return render(request, 'web/register.html')
                
                # Payment validation only for Non-NRCM
                if college_sel == 'OTHER':
                    if not trans_id or not request.FILES.get('payment_screenshot'):
                        print("DEBUGGING ERROR: Missing payment details for OTHER college.")
                        messages.error(request, "Payment details are required for non-NRCM students.")
                        return render(request, 'web/register.html')

                    if Registration.objects.filter(transaction_id=trans_id).exists():
                        print("DEBUGGING ERROR: Transaction ID already used.")
                        messages.error(request, "Transaction ID already used.")
                        return render(request, 'web/register.html')
                else:
                    if not trans_id:
                        trans_id = None 

                print("DEBUG: Creating Registration Object...")
                # Create Registration
                reg = Registration.objects.create(
                    project_title=project_title,
                    project_category=project_category, # NEW
                    selection_status='PENDING', # Fix for not-null constraint
                    team_leader_name=leader_name,
                    team_leader_email=leader_email,
                    team_leader_mobile=leader_mobile,
                    team_size=team_size,
                    college_selection=college_sel,
                    college_name_other=college_other,
                    transaction_id=trans_id,
                    payment_screenshot=request.FILES.get('payment_screenshot') if college_sel == 'OTHER' else None,
                    project_document=request.FILES.get('project_document')
                )
                print(f"DEBUG: Registration Created: {reg.id}")

                import re
                mobile_pattern = re.compile(r'^\d{10}$')

                # Create Team Members
                for i in range(1, team_size + 1):
                    name = request.POST.get(f'member_name_{i}')
                    email = request.POST.get(f'member_email_{i}')
                    mobile = request.POST.get(f'member_mobile_{i}')
                    roll = request.POST.get(f'member_roll_{i}')
                    dept = request.POST.get(f'member_dept_{i}')
                    tshirt = request.POST.get(f'member_tshirt_{i}')
                    food = request.POST.get(f'member_food_{i}')
                    
                    # Validation
                    if not mobile or not mobile_pattern.match(mobile):
                         raise ValueError(f"Member {i} mobile number must be exactly 10 digits.")
                    if not email or '@' not in email:
                         raise ValueError(f"Member {i} email is invalid.")

                    TeamMember.objects.create(
                        registration=reg,
                        name=name,
                        email=email,
                        mobile=mobile,
                        roll_no=roll,
                        department=dept,
                        tshirt_size=tshirt,
                        food_preference=food
                    )
                
                print("DEBUG: All team members created. Success!")
                messages.success(request, "Registration successful! Good luck for Ignite 2K26.")
                return redirect('success')

        except Exception as e:
            print(f"DEBUGGING ERROR: Exception occurred: {str(e)}")
            import traceback
            traceback.print_exc()
            messages.error(request, f"An error occurred: {str(e)}")
            return render(request, 'web/register.html')

    return render(request, 'web/register.html')


def success(request):
    return render(request, 'web/success.html')

from django.http import JsonResponse
from .models import GalleryImage

def gallery_api(request):
    images = GalleryImage.objects.all().order_by('-created_at')
    data = [
        {
            'url': img.image.url,
            'alt': img.alt_text or "Gallery Image"
        }
        for img in images
    ]
    return JsonResponse({'images': data})
