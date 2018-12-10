$(document).ready(function(){
  var selected_areas=[]
  $('.js-example-basic-multiple option:selected').each(function(){
    selected_areas.push($(this))
  })
  var selected_keywords=[]
  $('.js-example-basic-multiple2 option:selected').each(function(){
    selected_keywords.push($(this))
  })
  var maker1_click=0;
  var maker2_click=0;

  var keyword_options=[]
  var color=['#FF6633', '#FFB399', '#FF33FF', '#FFFF99', '#00B3E6',
		  '#E6B333', '#3366E6', '#999966', '#99FF99', '#B34D4D',
		  '#80B300', '#809900', '#E6B3B3', '#6680B3', '#66991A',
		  '#FF99E6', '#CCFF1A', '#FF1A66', '#E6331A', '#33FFCC',
		  '#66994D', '#B366CC', '#4D8000', '#B33300', '#CC80CC',
		  '#66664D', '#991AFF', '#E666FF', '#4DB3FF', '#1AB399',
		  '#E666B3', '#33991A', '#CC9999', '#B3B31A', '#00E680',
		  '#4D8066', '#809980', '#E6FF80', '#1AFF33', '#999933',
		  '#FF3380', '#CCCC00', '#66E64D', '#4D80CC', '#9900B3',
		  '#E64D66', '#4DB380', '#FF4D4D', '#99E6E6', '#6666FF']

      for (i=0;i<selected_areas.length;i++){
        var badge=$("<span style=\"background-color:"+color[maker1_click]+";\" class=\"button location_click_delete\">"+selected_areas[i].text()+"</span>")
        maker1_click++
        let area_value=selected_areas[i].val()
        $('.buttoning1').find("option[value='"+area_value+"']").prop('disabled','disabled')
        badge.click(function(){
          $(this).remove()
          $('.location').find("option[value='"+area_value+"']").prop("selected","").change()
          $('.buttoning1').find("option[value='"+area_value+"']").prop('disabled','').change()
        })

        $('.areas-container').append(badge)
      }

      for (i=0;i<selected_keywords.length;i++){
        var badge=$("<span style=\"background-color:"+color[maker1_click]+";\" class=\"button location_click_delete\">"+selected_keywords[i].text()+"</span>")
        maker1_click++
        let keyword_value=selected_keywords[i].val()
        $('.buttoning2').find("option[value='"+keyword_value+"']").prop('disabled','disabled')
        badge.click(function(){
          $(this).remove()
          $('.keyword').find("option[value='"+keyword_value+"']").prop("selected","").change()
          $('.buttoning2').find("option[value='"+keyword_value+"']").prop('disabled','').change()
        })
        $('.keywords-container').append(badge)
      }
  $('.button-maker1').click(function(){
    var value=$('.buttoning1 option:selected').val()
    $('.buttoning1 option:selected').prop('disabled','disabled')
    var badge=$("<span style=\"background-color:"+color[maker1_click]+";\" class=\"button location_click_delete\">"+$('.buttoning1 option:selected').text()+"</span>")
    maker1_click++
    badge.click(function(){
      $(this).remove()
      $('.location').find("option[value='"+value+"']").prop("selected","").change()
      $('.buttoning1').find("option[value='"+value+"']").prop('disabled','').change()
    })
    $('.areas-container').append(badge)
    $('.buttoning1').val("")
    $('.location').find("option[value='"+value+"']").prop("selected","selected").change()

  })




  $('.button-maker2').click(function(){
    var keyword=$('.buttoning2').val()

    var keyword_option=$("<option selected value=\""+keyword+"\">"+keyword+"</option>")
    keyword_options.push(keyword_option)
    $('.keyword').append(keyword_option)
    var badge=$("<span style=\"background-color:"+color[maker2_click]+";\" class=\"button\">"+$('.buttoning2').val()+"</span>")
    maker2_click++

    $('.keywords-container').append(badge)
    $('.buttoning2 option:selected').attr('disabled','disabled')
    $('.buttoning2').select2({
  tags: true
    });
    $('.buttoning2').val("")
    badge.click(function(){
      $(this).remove()
      keyword_option.remove()
      $('.buttoning2').find("option[value='"+keyword+"']").prop('disabled','').change()
    })

  })
  $('.messages').fadeOut(5000)
  $(".report-tweet").each(function () {
      $(this).modalForm({formURL: $(this).data('id')});
    });
  $("form").submit(function(){
    $('button[type=submit], input[type=submit]').prop('disabled',true);
  })


})
