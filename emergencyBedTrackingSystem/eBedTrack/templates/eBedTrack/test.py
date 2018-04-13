
@login_required
def patient_edit(request, pk):
    print('inside patient_edit')
    patient = get_object_or_404(Patient, pk=pk)
    print('patient bed id')
    print(patient.bed_id)
    print(request.method)
    if request.method == "POST":
        print('yes its post method')
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            print('form is valid')
            patient = form.save(commit=False)
            patient.updated_date = timezone.now()
            patient.save()
            s = form.cleaned_data.get('patient_status')
            if s=='Discharged':
                Pat=Patient.objects.filter(id=pk).values('bed_id')
                for i in Pat:
                    for k,v in i.items():
                        Bed.objects.filter(bed_id=v).update(status='VACANT')

            # patient = Patient.objects.filter(created_date__lte=timezone.now())
            patient = Patient.objects.filter(hospital_id=request.user.username)
            print('patient updated '+ str(patient))
            return render(request, 'eBedTrack/patient_list.html',
                         {'patients': patient})
        else:
            form = PatientForm(instance=patient)
            return render(request, 'eBedTrack/patient_edit.html', {'form':form })

    else:
        form = PatientForm(instance=patient)
        return render(request, 'eBedTrack/patient_edit.html', {'form': form})





