;----------------------------------------------------------------------
; This is a basic NCL template for creating XY plots.
;----------------------------------------------------------------------

; Note: as of NCL V6.2.0, you don't need these two load commands
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"

begin
;---Read data
  filename = "file.nc"
  a = addfile(filename,"r")
  x = a->x
  y = a->y

;---Open workstation
  wks = gsn_open_wks("x11","xy")   ; "ps", "pdf", "png"

;---Set some resources
  res                   = True

  res@gsnMaximize       = True     ; maximize plot in frame

;---These are sample resources you might want to set.
  res@xyLineColor       = "blue"   ; use xyLineColors if multiple lines
  res@xyLineThicknessF  = 2.5      ; default is 1.0
  res@xyDashPattern     = 2        ; default is 0 (solid line)

  res@xyMarkLineMode    = "MarkLines" ; "lines", "markers"
  res@xyMarker          = 16          ; default is 0 (asterisk)

  res@xyMonoDashPattern = True     ; if want solid lines for all curves

  res@tiMainString      = "Data file is " + filename

  plot = gsn_csm_xy(wks,x,y,res)   ; use gsn_csm_y if no X values.
end